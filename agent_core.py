
"""
Project Drishti - Agent Core (QueryAnalyzer with Specialized Tools)
===================================================================

This module implements the "tool-using" AI logic with two specialized agents:
1. Detective_Tool: Text-to-SQL for structured data queries
2. Interrogator_Tool: RAG (Retrieval Augmented Generation) for unstructured data

The Orchestrator calls these tools based on query intent.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine, text, inspect
import chromadb
from chromadb.config import Settings

from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment
load_dotenv()


class DetectiveTool:
    """
    Detective Tool: Text-to-SQL Agent
    
    Handles structured data queries by converting natural language to SQL,
    executing against the relational database, and returning results.
    """
    
    def __init__(self, database_url: str, llm):
        self.database_url = database_url
        self.engine = create_engine(database_url, echo=False)
        self.llm = llm
        logger.info("Detective Tool (Text-to-SQL) initialized")
    
    def get_schema_info(self) -> str:
        """Get database schema information for the LLM"""
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        
        schema_info = "DATABASE SCHEMA:\n\n"
        
        for table in tables:
            columns = inspector.get_columns(table)
            schema_info += f"Table: {table}\n"
            schema_info += "Columns:\n"
            for col in columns:
                schema_info += f"  - {col['name']} ({col['type']})\n"
            schema_info += "\n"
        
        return schema_info
    
    def execute_sql(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame"""
        try:
            with self.engine.connect() as conn:
                result = pd.read_sql(text(query), conn)
            return result
        except Exception as e:
            logger.error(f"SQL Execution error: {str(e)}")
            raise
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Main query function: Convert natural language to SQL and execute
        
        Args:
            question: Natural language query about structured data
            
        Returns:
            Dictionary with SQL query, results, and metadata
        """
        try:
            # Get schema for context
            schema = self.get_schema_info()
            
            # Prompt for SQL generation
            sql_prompt = f"""You are a SQL expert for forensic data analysis.

{schema}

User Question: {question}

Generate a valid SQL query to answer this question. 
Return ONLY the SQL query without any explanation or markdown formatting.
Use standard SQL syntax compatible with SQLite.

SQL Query:"""
            
            # Generate SQL using LLM
            response = self.llm.invoke(sql_prompt)
            sql_query = response.content.strip()
            
            # Clean up the SQL query
            sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
            
            logger.info(f"Generated SQL: {sql_query}")
            
            # Execute SQL
            df_result = self.execute_sql(sql_query)
            
            # Format results
            result = {
                'success': True,
                'sql_query': sql_query,
                'data': df_result.to_dict('records'),
                'row_count': len(df_result),
                'columns': list(df_result.columns),
                'summary': f"Found {len(df_result)} results"
            }
            
            logger.info(f"Query successful: {len(df_result)} rows returned")
            return result
            
        except Exception as e:
            logger.error(f"Detective Tool error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'data': [],
                'row_count': 0
            }


class InterrogatorTool:
    """
    Interrogator Tool: RAG (Retrieval Augmented Generation) Agent
    
    Handles unstructured data queries using semantic search over the vector database
    and generates contextual answers using retrieved documents.
    """
    
    def __init__(self, chroma_persist_dir: str, llm):
        self.chroma_persist_dir = chroma_persist_dir
        self.llm = llm
        
        self.chroma_client = chromadb.Client(Settings(
            persist_directory=chroma_persist_dir,
            anonymized_telemetry=False
        ))
        
        logger.info("Interrogator Tool (RAG) initialized")
    
    def get_collections(self) -> List[str]:
        """Get all available collections"""
        collections = self.chroma_client.list_collections()
        return [col.name for col in collections]
    
    def semantic_search(self, question: str, n_results: int = 5) -> List[Dict]:
        """Perform semantic search across all collections"""
        collections = self.get_collections()
        all_results = []
        
        for collection_name in collections:
            try:
                collection = self.chroma_client.get_collection(collection_name)
                results = collection.query(
                    query_texts=[question],
                    n_results=n_results
                )
                
                # Format results
                if results['documents'] and results['documents'][0]:
                    for i, doc in enumerate(results['documents'][0]):
                        all_results.append({
                            'document': doc,
                            'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                            'distance': results['distances'][0][i] if results['distances'] else 0,
                            'collection': collection_name
                        })
            except Exception as e:
                logger.warning(f"Error searching collection {collection_name}: {str(e)}")
        
        # Sort by relevance (distance)
        all_results.sort(key=lambda x: x.get('distance', 999))
        
        return all_results[:n_results]
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Main query function: Semantic search + RAG generation
        
        Args:
            question: Natural language query about unstructured data
            
        Returns:
            Dictionary with answer, source documents, and metadata
        """
        try:
            # Perform semantic search
            search_results = self.semantic_search(question, n_results=5)
            
            if not search_results:
                return {
                    'success': False,
                    'answer': "No relevant information found in the unstructured data.",
                    'sources': [],
                    'context_used': 0
                }
            
            # Build context from retrieved documents
            context = "\n\n".join([
                f"[Source: {r['metadata'].get('source', 'Unknown')}]\n{r['document']}"
                for r in search_results
            ])
            
            # RAG prompt
            rag_prompt = f"""You are a forensic analyst reviewing evidence from digital devices.

Context from Evidence Files:
{context}

User Question: {question}

Based ONLY on the evidence provided above, answer the question thoroughly.
If the evidence doesn't contain relevant information, say so clearly.
Cite specific sources when possible.

Answer:"""
            
            # Generate answer using LLM
            response = self.llm.invoke(rag_prompt)
            answer = response.content.strip()
            
            # Format sources
            sources = [
                {
                    'source': r['metadata'].get('source', 'Unknown'),
                    'relevance': f"{(1 - r['distance']):.2f}" if r.get('distance') else "N/A",
                    'excerpt': r['document'][:200] + "..."
                }
                for r in search_results
            ]
            
            result = {
                'success': True,
                'answer': answer,
                'sources': sources,
                'context_used': len(search_results)
            }
            
            logger.info(f"RAG query successful: {len(search_results)} documents used")
            return result
            
        except Exception as e:
            logger.error(f"Interrogator Tool error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'answer': "Error processing query",
                'sources': []
            }


class LinkAnalyzer:
    """
    Link Analysis Logic: Cross-references results from both tools
    
    This performs deterministic data correlation, not AI inference.
    Example: Filter chat messages to only those involving specific phone numbers.
    """
    
    @staticmethod
    def cross_reference(sql_results: List[Dict], rag_results: Dict) -> Dict[str, Any]:
        """
        Cross-reference structured and unstructured results
        
        Example use cases:
        - Find chats mentioning phone numbers from SQL results
        - Correlate locations with timeline events
        - Match names across different data sources
        """
        # Extract entities from SQL results
        entities = {
            'phone_numbers': set(),
            'names': set(),
            'locations': set(),
            'keywords': set()
        }
        
        for row in sql_results:
            # Extract phone numbers
            for key, value in row.items():
                if 'phone' in key.lower() or 'caller' in key.lower() or 'receiver' in key.lower():
                    if value:
                        entities['phone_numbers'].add(str(value))
                
                if 'name' in key.lower():
                    if value:
                        entities['names'].add(str(value))
                
                if 'location' in key.lower():
                    if value:
                        entities['locations'].add(str(value))
        
        # Check if entities appear in unstructured data
        rag_text = rag_results.get('answer', '')
        
        matches = {
            'phone_numbers': [p for p in entities['phone_numbers'] if p in rag_text],
            'names': [n for n in entities['names'] if n in rag_text],
            'locations': [l for l in entities['locations'] if l in rag_text]
        }
        
        return {
            'entities_found': entities,
            'cross_references': matches,
            'has_links': any(len(v) > 0 for v in matches.values())
        }


class QueryAnalyzer:
    """
    Main QueryAnalyzer: Orchestrates Detective and Interrogator tools
    
    This is called by the Orchestrator to execute queries using the appropriate tool(s).
    """
    
    def __init__(self, database_url: str, chroma_dir: str, api_key: str):
        # Initialize LLM - Using Gemini 2.5 Pro with Thinking Mode
        # Gemini 2.5 Pro features:
        # - State-of-the-art reasoning over complex problems
        # - 1M+ token context window for large datasets
        # - Thinking mode for step-by-step reasoning
        # - Advanced code execution and function calling
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            google_api_key=api_key,
            temperature=0.1,
            # Enable thinking mode for complex reasoning
            model_kwargs={
                "thinking_config": {
                    "thinking_budget": -1  # -1 = unlimited thinking
                }
            },
            # Increase max output tokens for detailed responses
            max_output_tokens=8192,
            # Enable safety for forensic content
            convert_system_message_to_human=True
        )
        
        # Initialize tools
        self.detective = DetectiveTool(database_url, self.llm)
        self.interrogator = InterrogatorTool(chroma_dir, self.llm)
        self.link_analyzer = LinkAnalyzer()
        
        logger.info("QueryAnalyzer initialized with Detective and Interrogator tools")
    
    def analyze_query_intent(self, query: str) -> Dict[str, bool]:
        """
        Determine which tools to use based on query intent
        
        Returns:
            Dictionary indicating whether to use SQL, RAG, or both
        """
        query_lower = query.lower()
        
        # Keywords suggesting structured data query
        sql_keywords = [
            'how many', 'count', 'list', 'show', 'filter', 'between',
            'after', 'before', 'duration', 'number', 'calls', 'messages',
            'transactions', 'total', 'sum', 'average', 'max', 'min'
        ]
        
        # Keywords suggesting unstructured data query
        rag_keywords = [
            'what did', 'conversation', 'chat', 'discuss', 'talk about',
            'mention', 'say', 'notes', 'details', 'context', 'why',
            'explain', 'describe'
        ]
        
        needs_sql = any(keyword in query_lower for keyword in sql_keywords)
        needs_rag = any(keyword in query_lower for keyword in rag_keywords)
        
        # If unclear, use both
        if not needs_sql and not needs_rag:
            needs_sql = needs_rag = True
        
        return {
            'use_detective': needs_sql,
            'use_interrogator': needs_rag
        }
    
    def execute_query(self, query: str) -> Dict[str, Any]:
        """
        Main execution function: Routes query to appropriate tool(s)
        
        Args:
            query: Natural language query from user
            
        Returns:
            Comprehensive results from tool(s) with link analysis
        """
        logger.info(f"Executing query: {query}")
        
        # Analyze intent
        intent = self.analyze_query_intent(query)
        logger.info(f"Query intent: {intent}")
        
        results = {
            'query': query,
            'intent': intent,
            'timestamp': datetime.now().isoformat()
        }
        
        # Execute Detective Tool (SQL)
        if intent['use_detective']:
            logger.info("Invoking Detective Tool (Text-to-SQL)...")
            results['detective_results'] = self.detective.query(query)
        
        # Execute Interrogator Tool (RAG)
        if intent['use_interrogator']:
            logger.info("Invoking Interrogator Tool (RAG)...")
            results['interrogator_results'] = self.interrogator.query(query)
        
        # Link Analysis (if both tools used)
        if intent['use_detective'] and intent['use_interrogator']:
            if results.get('detective_results', {}).get('success') and \
               results.get('interrogator_results', {}).get('success'):
                logger.info("Performing Link Analysis...")
                results['link_analysis'] = self.link_analyzer.cross_reference(
                    results['detective_results'].get('data', []),
                    results['interrogator_results']
                )
        
        return results


# Convenience function for testing
def test_query_analyzer():
    """Test the QueryAnalyzer with sample queries"""
    load_dotenv()
    
    database_url = os.getenv('DATABASE_URL', 'sqlite:///./drishti.db')
    chroma_dir = os.getenv('CHROMA_PERSIST_DIRECTORY', './chroma_db')
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not found in .env file")
        return
    
    analyzer = QueryAnalyzer(database_url, chroma_dir, api_key)
    
    # Test queries
    test_queries = [
        "How many calls were made after 10 PM?",
        "What did the suspects discuss in WhatsApp?",
        "Show me all financial transactions over 1 lakh"
    ]
    
    for query in test_queries:
        print(f"\n{'='*70}")
        print(f"Query: {query}")
        print(f"{'='*70}")
        
        results = analyzer.execute_query(query)
        print(f"Results: {results}")


if __name__ == "__main__":
    test_query_analyzer()
