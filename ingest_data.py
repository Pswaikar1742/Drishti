"""
Project Drishti - Processor Agent (Offline Data Ingestion)
===========================================================

This script processes UFDR (Universal Forensic Extraction Device Report) data
and ingests it into both SQL (structured) and Vector (unstructured) databases.

The Hybrid Intelligence Architecture:
- Structured data (CSV files) → SQLite database → Text-to-SQL queries
- Unstructured data (TXT files) → ChromaDB vector database → Semantic search

Usage:
    python ingest_data.py --path /path/to/ufdr_folder
    python ingest_data.py --path /path/to/ufdr.zip
"""

import os
import sys
import argparse
import logging
import zipfile
import shutil
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine, inspect, MetaData, Table, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import sessionmaker
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UFDRProcessor:
    """
    UFDR Data Processor - Implements the Hybrid Intelligence Architecture
    
    This processor intelligently routes data:
    - Structured files (CSV) → SQL Database (for precise filtering)
    - Unstructured files (TXT) → Vector Database (for semantic search)
    """
    
    def __init__(self, database_url: str, chroma_persist_dir: str):
        """Initialize processor with database connections"""
        self.database_url = database_url
        self.chroma_persist_dir = chroma_persist_dir
        
        # SQL Database setup
        self.engine = create_engine(database_url, echo=False)
        self.metadata = MetaData()
        
        # Vector Database setup
        self.chroma_client = chromadb.Client(Settings(
            persist_directory=chroma_persist_dir,
            anonymized_telemetry=False
        ))
        
        # File type mappings
        self.structured_files = [
            'CallLogs.csv', 'Contacts.csv', 'SMS_Messages.csv',
            'Location_History.csv', 'Browser_History.csv', 'App_Usage.csv',
            'Email_Records.csv', 'Bank_Transactions.csv', 'Calendar_Events.csv',
            'Photos_Metadata.csv', 'Social_Media_Activity.csv', 'WiFi_Connections.csv',
            'Bluetooth_Devices.csv', 'File_System_Events.csv',
            'Audio_Recordings_Metadata.csv', 'Video_Recordings_Metadata.csv'
        ]
        
        self.unstructured_files = [
            'WhatsApp_Chats.txt', 'Notes.txt', 'Device_Info.txt',
            'Suspicious_Keywords.txt'
        ]
        
        logger.info("UFDR Processor initialized")
        logger.info(f"SQL Database: {database_url}")
        logger.info(f"Vector Database: {chroma_persist_dir}")
    
    def extract_zip(self, zip_path: str, extract_to: str) -> str:
        """Extract ZIP file to temporary directory"""
        logger.info(f"Extracting ZIP file: {zip_path}")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        logger.info(f"Extracted to: {extract_to}")
        return extract_to
    
    def find_ufdr_files(self, root_path: str) -> Dict[str, List[str]]:
        """Recursively find all UFDR files and categorize them"""
        structured = []
        unstructured = []
        
        for root, dirs, files in os.walk(root_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                if file in self.structured_files:
                    structured.append(file_path)
                    logger.debug(f"Found structured file: {file}")
                elif file in self.unstructured_files:
                    unstructured.append(file_path)
                    logger.debug(f"Found unstructured file: {file}")
        
        logger.info(f"Found {len(structured)} structured files")
        logger.info(f"Found {len(unstructured)} unstructured files")
        
        return {
            'structured': structured,
            'unstructured': unstructured
        }
    
    def clean_table_name(self, filename: str) -> str:
        """Convert filename to valid SQL table name"""
        table_name = Path(filename).stem.lower()
        table_name = table_name.replace(' ', '_').replace('-', '_')
        return table_name
    
    def ingest_structured_data(self, file_path: str):
        """Ingest CSV files into SQL database"""
        try:
            filename = os.path.basename(file_path)
            table_name = self.clean_table_name(filename)
            
            logger.info(f"Processing structured file: {filename} → Table: {table_name}")
            
            # Read CSV with error handling
            df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
            
            if df.empty:
                logger.warning(f"Empty dataframe for {filename}, skipping")
                return
            
            # Clean column names
            df.columns = [col.lower().replace(' ', '_').replace('(', '').replace(')', '') 
                         for col in df.columns]
            
            # Convert datetime columns if they contain 'timestamp' or 'date'
            for col in df.columns:
                if 'timestamp' in col or 'date' in col or 'time' in col:
                    try:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                    except:
                        pass
            
            # Ingest into database using SQLAlchemy (production-ready abstraction)
            df.to_sql(
                table_name,
                self.engine,
                if_exists='replace',
                index=False,
                method='multi',
                chunksize=1000
            )
            
            logger.info(f"✓ Ingested {len(df)} rows into '{table_name}' table")
            
        except Exception as e:
            logger.error(f"✗ Error processing {file_path}: {str(e)}")
    
    def ingest_unstructured_data(self, file_path: str, case_id: str):
        """Ingest text files into vector database for semantic search"""
        try:
            filename = os.path.basename(file_path)
            logger.info(f"Processing unstructured file: {filename}")
            
            # Read text file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if not content.strip():
                logger.warning(f"Empty content for {filename}, skipping")
                return
            
            # Split content into chunks for better semantic search
            chunks = self.chunk_text(content, chunk_size=500)
            
            # Get or create collection
            collection_name = f"ufdr_{case_id}"
            try:
                collection = self.chroma_client.get_collection(collection_name)
            except:
                collection = self.chroma_client.create_collection(
                    name=collection_name,
                    metadata={"description": f"UFDR case {case_id}"}
                )
            
            # Add documents to vector database
            for i, chunk in enumerate(chunks):
                doc_id = f"{filename}_{i}"
                collection.add(
                    documents=[chunk],
                    metadatas=[{
                        "source": filename,
                        "chunk_id": i,
                        "case_id": case_id
                    }],
                    ids=[doc_id]
                )
            
            logger.info(f"✓ Ingested {len(chunks)} chunks from '{filename}' into vector DB")
            
        except Exception as e:
            logger.error(f"✗ Error processing {file_path}: {str(e)}")
    
    def chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """Split text into overlapping chunks for better context"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size + 50])  # 50 word overlap
            chunks.append(chunk)
        
        return chunks if chunks else [text]
    
    def process_ufdr_folder(self, ufdr_path: str, case_id: Optional[str] = None):
        """Main processing function - implements Hybrid Intelligence routing"""
        
        # Generate case ID if not provided
        if not case_id:
            case_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        logger.info("="*70)
        logger.info("UFDR PROCESSOR - HYBRID INTELLIGENCE ARCHITECTURE")
        logger.info("="*70)
        logger.info(f"Case ID: {case_id}")
        logger.info(f"Source: {ufdr_path}")
        
        # Handle ZIP files
        temp_extract_dir = None
        if ufdr_path.endswith('.zip'):
            temp_extract_dir = f"./temp_extraction_{case_id}"
            os.makedirs(temp_extract_dir, exist_ok=True)
            ufdr_path = self.extract_zip(ufdr_path, temp_extract_dir)
        
        # Find all UFDR files
        files = self.find_ufdr_files(ufdr_path)
        
        # Process Structured Data → SQL Database
        logger.info("\n" + "="*70)
        logger.info("PHASE 1: STRUCTURED DATA → SQL DATABASE")
        logger.info("="*70)
        
        for file_path in files['structured']:
            self.ingest_structured_data(file_path)
        
        # Process Unstructured Data → Vector Database
        logger.info("\n" + "="*70)
        logger.info("PHASE 2: UNSTRUCTURED DATA → VECTOR DATABASE")
        logger.info("="*70)
        
        for file_path in files['unstructured']:
            self.ingest_unstructured_data(file_path, case_id)
        
        # Cleanup
        if temp_extract_dir and os.path.exists(temp_extract_dir):
            shutil.rmtree(temp_extract_dir)
            logger.info(f"Cleaned up temporary directory: {temp_extract_dir}")
        
        # Summary
        logger.info("\n" + "="*70)
        logger.info("INGESTION COMPLETE")
        logger.info("="*70)
        logger.info(f"Structured files processed: {len(files['structured'])}")
        logger.info(f"Unstructured files processed: {len(files['unstructured'])}")
        logger.info(f"Case ID: {case_id}")
        logger.info("="*70)
        
        return case_id
    
    def list_tables(self):
        """List all tables in the SQL database"""
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        
        logger.info("\nAvailable SQL Tables:")
        for table in tables:
            logger.info(f"  - {table}")
        
        return tables


def main():
    """Command-line interface for the processor"""
    parser = argparse.ArgumentParser(
        description='Project Drishti - UFDR Data Processor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ingest_data.py --path ./ufdr_sample_reports/case_001_cyber_fraud_ring
  python ingest_data.py --path ./my_ufdr_case.zip --case-id CASE_2025_001
        """
    )
    
    parser.add_argument(
        '--path',
        required=True,
        help='Path to UFDR folder or ZIP file'
    )
    
    parser.add_argument(
        '--case-id',
        help='Optional case ID (auto-generated if not provided)'
    )
    
    parser.add_argument(
        '--list-tables',
        action='store_true',
        help='List all tables after ingestion'
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    database_url = os.getenv('DATABASE_URL', 'sqlite:///./drishti.db')
    chroma_dir = os.getenv('CHROMA_PERSIST_DIRECTORY', './chroma_db')
    
    # Validate path
    if not os.path.exists(args.path):
        logger.error(f"Path does not exist: {args.path}")
        sys.exit(1)
    
    # Create processor and run
    processor = UFDRProcessor(database_url, chroma_dir)
    case_id = processor.process_ufdr_folder(args.path, args.case_id)
    
    if args.list_tables:
        processor.list_tables()
    
    logger.info(f"\n✓ Case '{case_id}' successfully ingested!")
    logger.info(f"You can now query this data using the main application.")


if __name__ == "__main__":
    main()
