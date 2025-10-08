"""
Project Drishti - Main Application
==================================

This file contains:
1. FastAPI Backend (REST API for the Orchestrator)
2. Streamlit Frontend (User Interface)
3. Orchestrator Logic (Central nervous system)

The application provides a web interface for uploading UFDR files and
querying them using natural language through the Hybrid Intelligence system.
"""

import os
import sys
import logging
import shutil
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

# Import our custom modules
from ingest_data import UFDRProcessor
from agent_core import QueryAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class Orchestrator:
    """
    Orchestrator Agent: The central nervous system
    
    Responsibilities:
    - Receive user queries from UI
    - Deconstruct query intent
    - Delegate to QueryAnalyzer tools
    - Synthesize and format results
    """
    
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL', 'sqlite:///./drishti.db')
        self.chroma_dir = os.getenv('CHROMA_PERSIST_DIRECTORY', './chroma_db')
        self.api_key = os.getenv('GOOGLE_API_KEY')
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables!")
        
        # Initialize QueryAnalyzer
        self.query_analyzer = QueryAnalyzer(
            self.database_url,
            self.chroma_dir,
            self.api_key
        )
        
        # Initialize UFDR Processor for uploads
        self.ufdr_processor = UFDRProcessor(
            self.database_url,
            self.chroma_dir
        )
        
        logger.info("Orchestrator initialized")
    
    def process_uploaded_ufdr(self, file_path: str, case_id: Optional[str] = None) -> Dict[str, Any]:
        """Process uploaded UFDR file"""
        try:
            logger.info(f"Processing uploaded UFDR: {file_path}")
            
            case_id = self.ufdr_processor.process_ufdr_folder(file_path, case_id)
            
            return {
                'success': True,
                'case_id': case_id,
                'message': f'Successfully processed case {case_id}'
            }
        except Exception as e:
            logger.error(f"Error processing UFDR: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def handle_query(self, query: str) -> Dict[str, Any]:
        """
        Main orchestration function: Handle user query
        
        This is where the magic happens:
        1. Receive query from UI
        2. Delegate to QueryAnalyzer
        3. Format and return results
        """
        try:
            logger.info(f"Orchestrator received query: {query}")
            
            # Delegate to QueryAnalyzer
            results = self.query_analyzer.execute_query(query)
            
            # Add orchestrator metadata
            results['orchestrator_timestamp'] = datetime.now().isoformat()
            results['status'] = 'success'
            
            return results
            
        except Exception as e:
            logger.error(f"Orchestrator error: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'query': query
            }


# ============================================================================
# STREAMLIT FRONTEND
# ============================================================================

def init_session_state():
    """Initialize Streamlit session state"""
    if 'orchestrator' not in st.session_state:
        try:
            st.session_state.orchestrator = Orchestrator()
            st.session_state.initialized = True
        except Exception as e:
            st.session_state.initialized = False
            st.session_state.error = str(e)
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'current_case_id' not in st.session_state:
        st.session_state.current_case_id = None


def render_header():
    """Render application header"""
    st.set_page_config(
        page_title="Project Drishti - UFDR Analysis",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🔍 Project Drishti (Insight)")
    st.markdown("### AI-Powered UFDR Analysis Tool")
    st.markdown("*Conversational Intelligence for Forensic Investigations*")
    st.divider()


def render_sidebar():
    """Render sidebar with file upload and configuration"""
    with st.sidebar:
        st.header("📁 UFDR Upload")
        st.markdown("Upload your UFDR report (ZIP or folder)")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose UFDR ZIP file",
            type=['zip'],
            help="Upload a UFDR export ZIP file"
        )
        
        case_id = st.text_input(
            "Case ID (optional)",
            placeholder="AUTO-GENERATED",
            help="Leave blank for auto-generated ID"
        )
        
        if uploaded_file is not None:
            if st.button("🚀 Process UFDR", type="primary"):
                with st.spinner("Processing UFDR file..."):
                    # Save uploaded file temporarily
                    temp_dir = tempfile.mkdtemp()
                    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
                    
                    with open(temp_file_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Process UFDR
                    result = st.session_state.orchestrator.process_uploaded_ufdr(
                        temp_file_path,
                        case_id if case_id else None
                    )
                    
                    # Cleanup
                    shutil.rmtree(temp_dir)
                    
                    if result['success']:
                        st.success(f"✅ {result['message']}")
                        st.session_state.current_case_id = result['case_id']
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        st.divider()
        
        # Quick access to sample cases
        st.header("📊 Sample Cases")
        st.markdown("Try our pre-loaded sample cases:")
        
        sample_cases = {
            "Cyber Fraud Ring": "./ufdr_sample_reports/case_001_cyber_fraud_ring",
            "Drug Trafficking": "./ufdr_sample_reports/case_002_drug_trafficking",
            "Terrorism Network": "./ufdr_sample_reports/case_003_terrorism_network"
        }
        
        for case_name, case_path in sample_cases.items():
            if os.path.exists(case_path):
                if st.button(f"📂 Load {case_name}", key=f"load_{case_name}"):
                    with st.spinner(f"Loading {case_name}..."):
                        result = st.session_state.orchestrator.process_uploaded_ufdr(case_path)
                        if result['success']:
                            st.success(f"✅ Loaded {case_name}")
                            st.session_state.current_case_id = result['case_id']
        
        st.divider()
        
        # System info
        st.header("ℹ️ System Info")
        if st.session_state.current_case_id:
            st.info(f"**Active Case:** {st.session_state.current_case_id}")
        else:
            st.warning("No case loaded")
        
        # Architecture info
        with st.expander("🧠 Hybrid Intelligence"):
            st.markdown("""
            **Two-Stream Processing:**
            - 🗄️ **SQL**: Structured data (CallLogs, SMS, etc.)
            - 🔍 **Vector DB**: Unstructured data (Chats, Notes)
            
            **AI Agents:**
            - 🕵️ Detective: Text-to-SQL queries
            - 💬 Interrogator: Semantic search (RAG)
            - 🔗 Link Analyzer: Cross-referencing
            """)


def render_query_interface():
    """Render main query interface"""
    st.header("💬 Ask Questions")
    st.markdown("Ask questions about the evidence in natural language")
    
    # Example queries
    with st.expander("💡 Example Queries"):
        st.markdown("""
        **Structured Queries (SQL):**
        - How many calls were made after 10 PM?
        - Show me all financial transactions over ₹1 lakh
        - List all contacts without saved names
        - What is the total duration of calls to a specific number?
        
        **Unstructured Queries (RAG):**
        - What did the suspects discuss in WhatsApp?
        - Summarize the investigative notes
        - What are the key findings from device info?
        
        **Complex Queries (Both):**
        - Find all communications involving people who made suspicious transactions
        - Show me the timeline of events with context from chats
        """)
    
    # Query input
    query = st.text_input(
        "Your Question:",
        placeholder="e.g., Show me all calls after 10 PM to unknown numbers",
        key="query_input"
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        submit_button = st.button("🔍 Analyze", type="primary")
    
    with col2:
        clear_button = st.button("🗑️ Clear History")
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()
    
    # Process query
    if submit_button and query:
        if not st.session_state.current_case_id:
            st.warning("⚠️ Please load a UFDR case first!")
        else:
            with st.spinner("🤔 Analyzing..."):
                results = st.session_state.orchestrator.handle_query(query)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    'query': query,
                    'results': results,
                    'timestamp': datetime.now()
                })
                
                # Display results
                render_results(results)
    
    # Display chat history
    if st.session_state.chat_history:
        st.divider()
        st.header("📜 Query History")
        
        for i, item in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(
                f"🕐 {item['timestamp'].strftime('%H:%M:%S')} - {item['query'][:60]}...",
                expanded=(i == 0)
            ):
                render_results(item['results'])


def render_results(results: Dict[str, Any]):
    """
    Render investigation results in a forensic-friendly format
    Output designed for investigators, court documentation, and case reporting
    """
    
    if results.get('status') == 'error':
        st.error(f"❌ Investigation Error: {results.get('error', 'Unknown error')}")
        st.info("💡 **Tip**: Try rephrasing your question or check if the data source is available.")
        return
    
    # Executive Summary Section
    st.markdown("## 📋 Investigation Summary")
    
    intent = results.get('intent', {})
    detective_active = intent.get('use_detective', False)
    interrogator_active = intent.get('use_interrogator', False)
    
    # Analysis method indicators
    col1, col2, col3 = st.columns([2, 2, 3])
    with col1:
        if detective_active:
            st.success("🔍 **Database Analysis**: Active")
        else:
            st.info("🔍 **Database Analysis**: Not needed")
    
    with col2:
        if interrogator_active:
            st.success("📄 **Document Analysis**: Active")
        else:
            st.info("📄 **Document Analysis**: Not needed")
    
    with col3:
        evidence_count = 0
        if 'detective_results' in results:
            evidence_count += results['detective_results'].get('row_count', 0)
        if 'interrogator_results' in results:
            sources = results.get('interrogator_results', {}).get('sources', [])
            evidence_count += len(sources)
        st.metric("📊 Evidence Items Found", evidence_count)
    
    st.markdown("---")
    
    # Detective Results (Database/SQL) - Investigation Format
    if 'detective_results' in results:
        st.markdown("## 🕵️ Database Evidence")
        detective = results['detective_results']
        
        if detective.get('success'):
            record_count = detective.get('row_count', 0)
            
            if record_count > 0:
                st.success(f"✅ **{record_count} records found** matching your investigation criteria")
                
                data = detective.get('data', [])
                if data:
                    df = pd.DataFrame(data)
                    
                    # Show key findings summary
                    st.markdown("### 📌 Key Findings")
                    
                    # Automatic insight generation
                    insights = []
                    
                    # Check for temporal patterns
                    timestamp_cols = [col for col in df.columns if 'timestamp' in col.lower() or 'date' in col.lower() or 'time' in col.lower()]
                    if timestamp_cols:
                        try:
                            ts_col = timestamp_cols[0]
                            df_temp = df.copy()
                            df_temp[ts_col] = pd.to_datetime(df_temp[ts_col], errors='coerce')
                            df_temp = df_temp.dropna(subset=[ts_col])
                            if len(df_temp) > 0:
                                date_range = (df_temp[ts_col].max() - df_temp[ts_col].min()).days
                                insights.append(f"� Evidence spans **{date_range} days** (from {df_temp[ts_col].min().strftime('%Y-%m-%d')} to {df_temp[ts_col].max().strftime('%Y-%m-%d')})")
                                
                                # Late night activity check
                                df_temp['hour'] = df_temp[ts_col].dt.hour
                                late_night = df_temp[(df_temp['hour'] >= 22) | (df_temp['hour'] <= 5)]
                                if len(late_night) > 0:
                                    pct = (len(late_night) / len(df_temp)) * 100
                                    insights.append(f"🌙 **{len(late_night)} events ({pct:.1f}%)** occurred during late night hours (10 PM - 5 AM)")
                        except:
                            pass
                    
                    # Check for numeric patterns
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    if numeric_cols and len(numeric_cols) > 0:
                        for col in numeric_cols[:2]:  # Analyze first 2 numeric columns
                            total = df[col].sum()
                            avg = df[col].mean()
                            insights.append(f"📊 {col.replace('_', ' ').title()}: Total = {total:,.2f}, Average = {avg:,.2f}")
                    
                    # Check for categorical patterns
                    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                    if categorical_cols:
                        for col in categorical_cols[:2]:  # Analyze first 2 categorical columns
                            unique_count = df[col].nunique()
                            if unique_count <= 20:
                                top_value = df[col].value_counts().iloc[0]
                                top_name = df[col].value_counts().index[0]
                                insights.append(f"👤 Most frequent {col.replace('_', ' ')}: **{top_name}** ({top_value} occurrences)")
                    
                    # Display insights
                    if insights:
                        for insight in insights:
                            st.markdown(f"- {insight}")
                    else:
                        st.info("Review the data table and visualizations below for patterns")
                    
                    st.markdown("---")
                    
                    # Show data table
                    st.markdown("### 📊 Evidence Records")
                    st.markdown(f"*{len(df)} records retrieved from database*")
                    st.dataframe(df, use_container_width=True, height=400)
                    
                    # Visualizations
                    if len(df) > 0 and len(df.columns) > 1:
                        render_visualizations(df)
                    
                    # Technical details (collapsed)
                    with st.expander("🔧 Technical Details (SQL Query)"):
                        st.caption("*This section contains technical database information for advanced users*")
                        st.code(detective.get('sql_query', ''), language='sql')
                        st.caption(f"Query executed successfully. Returned {record_count} rows.")
                
            else:
                st.warning("⚠️ **No records found** matching your criteria")
                st.info("💡 Try:\n- Broadening your search criteria\n- Checking date ranges\n- Verifying names or phone numbers")
        
        else:
            st.error(f"❌ **Database query failed**: {detective.get('error', 'Unknown error')}")
            st.info("💡 This might be due to invalid search criteria or database connection issues")
            
            # Show technical error details (collapsed)
            with st.expander("🔧 Error Details"):
                st.code(detective.get('sql_query', 'No query generated'), language='sql')
                st.caption(detective.get('error', 'Unknown error'))
    
    # Interrogator Results (Documents/RAG) - Investigation Format
    if 'interrogator_results' in results:
        st.markdown("## � Document Evidence")
        interrogator = results['interrogator_results']
        
        if interrogator.get('success'):
            # Show main finding/answer
            answer = interrogator.get('answer', 'No answer generated')
            
            st.markdown("### 🎯 Investigation Finding")
            st.success(answer)
            
            # Show source documents
            sources = interrogator.get('sources', [])
            if sources:
                st.markdown(f"### 📚 Supporting Evidence ({len(sources)} documents)")
                st.markdown("*Documents that contain relevant information*")
                
                for i, source in enumerate(sources, 1):
                    with st.expander(f"📑 Evidence Document {i}: {source['source']}", expanded=(i == 1)):
                        st.markdown(f"**Relevance Score**: {source['relevance']}")
                        st.markdown("**Excerpt:**")
                        st.info(source['excerpt'])
                        st.caption(f"*Source: {source['source']}*")
            else:
                st.info("No supporting documents found")
        
        else:
            st.error(f"❌ **Document analysis failed**: {interrogator.get('error', 'Unknown error')}")
            st.info("💡 Try rephrasing your question or check if relevant documents are available")
    
    # Link Analysis
    if 'link_analysis' in results:
        st.markdown("### 🔗 Link Analysis")
        links = results['link_analysis']
        
        if links.get('has_links'):
            st.success("✅ Cross-references found!")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                phone_matches = links['cross_references'].get('phone_numbers', [])
                st.metric("Phone Numbers", len(phone_matches))
                if phone_matches:
                    st.caption(", ".join(phone_matches[:3]))
            
            with col2:
                name_matches = links['cross_references'].get('names', [])
                st.metric("Names", len(name_matches))
                if name_matches:
                    st.caption(", ".join(name_matches[:3]))
            
            with col3:
                location_matches = links['cross_references'].get('locations', [])
                st.metric("Locations", len(location_matches))
                if location_matches:
                    st.caption(", ".join(location_matches[:3]))
        else:
            st.info("No cross-references found between structured and unstructured data")


def render_visualizations(df: pd.DataFrame):
    """
    Generate forensic-friendly visualizations
    Designed for investigators, not computer scientists
    """
    if df.empty or len(df) == 0:
        return
    
    st.markdown("### 📊 Visual Evidence Analysis")
    st.markdown("*Charts generated for investigative reporting*")
    
    # Detect column types
    timestamp_cols = [col for col in df.columns if 'timestamp' in col.lower() or 'date' in col.lower() or 'time' in col.lower()]
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Timeline", "📊 Distribution", "🔥 Heat Map", "📉 Statistics"])
    
    with tab1:
        st.markdown("#### Timeline Analysis")
        if timestamp_cols and len(df) > 1:
            try:
                ts_col = timestamp_cols[0]
                df_copy = df.copy()
                df_copy[ts_col] = pd.to_datetime(df_copy[ts_col], errors='coerce')
                df_copy = df_copy.dropna(subset=[ts_col])
                
                if len(df_copy) > 0:
                    # Timeline with all events
                    if len(numeric_cols) > 0:
                        fig = px.scatter(df_copy, x=ts_col, y=numeric_cols[0],
                                       title=f"⏰ Event Timeline - {len(df_copy)} Events",
                                       labels={ts_col: "Time", numeric_cols[0]: numeric_cols[0].replace('_', ' ').title()},
                                       color_discrete_sequence=['#FF4B4B'])
                        fig.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')))
                    else:
                        # Just show event occurrences
                        df_copy['Event'] = 1
                        fig = px.scatter(df_copy, x=ts_col, y='Event',
                                       title=f"⏰ Event Timeline - {len(df_copy)} Events",
                                       labels={ts_col: "Time"},
                                       color_discrete_sequence=['#FF4B4B'])
                    
                    fig.update_layout(
                        height=400,
                        showlegend=False,
                        xaxis_title="Date & Time",
                        yaxis_title="Events",
                        font=dict(size=12),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Hour-of-day analysis
                    df_copy['hour'] = df_copy[ts_col].dt.hour
                    hourly_counts = df_copy['hour'].value_counts().sort_index()
                    
                    fig2 = px.bar(x=hourly_counts.index, y=hourly_counts.values,
                                 title="🕐 Activity by Hour of Day",
                                 labels={'x': 'Hour (24-hour format)', 'y': 'Number of Events'},
                                 color=hourly_counts.values,
                                 color_continuous_scale='Reds')
                    fig2.update_layout(showlegend=False, height=300)
                    st.plotly_chart(fig2, use_container_width=True)
                    
                    # Day of week analysis
                    df_copy['day_name'] = df_copy[ts_col].dt.day_name()
                    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    day_counts = df_copy['day_name'].value_counts().reindex(day_order, fill_value=0)
                    
                    fig3 = px.bar(x=day_counts.index, y=day_counts.values,
                                 title="📅 Activity by Day of Week",
                                 labels={'x': 'Day', 'y': 'Number of Events'},
                                 color=day_counts.values,
                                 color_continuous_scale='Blues')
                    fig3.update_layout(showlegend=False, height=300)
                    st.plotly_chart(fig3, use_container_width=True)
                    
            except Exception as e:
                st.info("⏱️ No timestamp data available for timeline analysis")
        else:
            st.info("⏱️ No timestamp data available for timeline visualization")
    
    with tab2:
        st.markdown("#### Distribution & Frequency Analysis")
        
        # Categorical distribution
        if categorical_cols:
            try:
                # Pick first categorical column
                cat_col = categorical_cols[0]
                value_counts = df[cat_col].value_counts().head(15)
                
                if len(value_counts) > 0:
                    fig = px.bar(x=value_counts.index, y=value_counts.values,
                               title=f"📊 {cat_col.replace('_', ' ').title()} Distribution",
                               labels={'x': cat_col.replace('_', ' ').title(), 'y': 'Count'},
                               color=value_counts.values,
                               color_continuous_scale='Viridis')
                    fig.update_layout(
                        height=400,
                        showlegend=False,
                        xaxis={'categoryorder':'total descending'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Pie chart for top categories
                    if len(value_counts) <= 10:
                        fig2 = px.pie(values=value_counts.values, names=value_counts.index,
                                     title=f"🥧 {cat_col.replace('_', ' ').title()} Breakdown")
                        st.plotly_chart(fig2, use_container_width=True)
            except:
                pass
        
        # Numeric distribution
        if numeric_cols:
            try:
                num_col = numeric_cols[0]
                fig = px.histogram(df, x=num_col,
                                 title=f"📈 {num_col.replace('_', ' ').title()} Distribution",
                                 labels={num_col: num_col.replace('_', ' ').title()},
                                 color_discrete_sequence=['#00CC96'])
                fig.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            except:
                pass
    
    with tab3:
        st.markdown("#### Heat Map Analysis")
        if timestamp_cols and len(df) > 5:
            try:
                ts_col = timestamp_cols[0]
                df_copy = df.copy()
                df_copy[ts_col] = pd.to_datetime(df_copy[ts_col], errors='coerce')
                df_copy = df_copy.dropna(subset=[ts_col])
                
                if len(df_copy) > 0:
                    # Hour vs Day heat map
                    df_copy['hour'] = df_copy[ts_col].dt.hour
                    df_copy['day_name'] = df_copy[ts_col].dt.day_name()
                    
                    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    pivot_data = df_copy.groupby(['day_name', 'hour']).size().reset_index(name='count')
                    pivot_table = pivot_data.pivot(index='day_name', columns='hour', values='count').fillna(0)
                    pivot_table = pivot_table.reindex(day_order)
                    
                    fig = px.imshow(pivot_table,
                                   title="🔥 Activity Heat Map: Hour vs Day of Week",
                                   labels=dict(x="Hour of Day", y="Day of Week", color="Activity Count"),
                                   color_continuous_scale='RdYlGn',
                                   aspect='auto')
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.info("🔍 **Forensic Insight**: Darker colors indicate higher activity. Look for unusual patterns (late night activity, weekend spikes, etc.)")
            except:
                st.info("🔥 Heat map requires sufficient temporal data")
        else:
            st.info("🔥 Heat map requires timestamp data")
    
    with tab4:
        st.markdown("#### Statistical Summary")
        
        # Key statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Total Records", len(df))
            if timestamp_cols:
                try:
                    ts_col = timestamp_cols[0]
                    df_temp = df.copy()
                    df_temp[ts_col] = pd.to_datetime(df_temp[ts_col], errors='coerce')
                    date_range = (df_temp[ts_col].max() - df_temp[ts_col].min()).days
                    st.metric("📅 Date Range", f"{date_range} days")
                except:
                    pass
        
        with col2:
            st.metric("📋 Data Fields", len(df.columns))
            if numeric_cols:
                st.metric("🔢 Numeric Fields", len(numeric_cols))
        
        with col3:
            if categorical_cols:
                st.metric("📝 Text Fields", len(categorical_cols))
                unique_count = df[categorical_cols[0]].nunique()
                st.metric(f"Unique {categorical_cols[0]}", unique_count)
        
        # Numeric summary
        if numeric_cols:
            st.markdown("##### 📐 Numerical Analysis")
            numeric_df = df[numeric_cols].describe().T
            numeric_df.columns = ['Count', 'Mean', 'Std Dev', 'Min', '25%', 'Median', '75%', 'Max']
            st.dataframe(numeric_df.style.format("{:.2f}"), use_container_width=True)
        
        # Top values
        if categorical_cols:
            st.markdown(f"##### 🔝 Top {categorical_cols[0].replace('_', ' ').title()} Values")
            top_values = df[categorical_cols[0]].value_counts().head(10)
            st.dataframe(top_values.reset_index().rename(columns={'index': categorical_cols[0], categorical_cols[0]: 'Count'}), 
                        use_container_width=True)
    
    # Export button
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col2:
        csv = df.to_csv(index=False)
        # Generate unique key based on data hash and timestamp
        import hashlib
        data_hash = hashlib.md5(csv.encode()).hexdigest()[:8]
        unique_key = f"download_{data_hash}_{datetime.now().strftime('%H%M%S')}"
        
        st.download_button(
            label="📥 Export Data (CSV)",
            data=csv,
            file_name=f"forensic_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download this data for court documentation",
            key=unique_key
        )


def main():
    """Main application entry point"""
    
    # Initialize
    init_session_state()
    
    # Check initialization
    if not st.session_state.get('initialized', False):
        st.error(f"❌ Initialization Error: {st.session_state.get('error', 'Unknown error')}")
        st.info("Please check your .env file and ensure GOOGLE_API_KEY is set correctly")
        st.stop()
    
    # Render UI
    render_header()
    render_sidebar()
    render_query_interface()
    
    # Footer
    st.divider()
    st.caption("Project Drishti v1.0 | Hybrid Intelligence Architecture | SQLite (Prototype) → PostgreSQL (Production)")


if __name__ == "__main__":
    main()
