# Project Drishti - Architecture Documentation

## Overview

Project Drishti implements a **Hybrid Intelligence Architecture** that recognizes different data types require different AI approaches. This document details the complete system architecture.

## Core Architectural Principles

### 1. Data-Type Aware Processing

The system automatically routes data based on its structure:

```
UFDR Data Input
    │
    ├─── Structured? (CSV) ──→ SQL Database ──→ Text-to-SQL Agent
    │
    └─── Unstructured? (TXT) ──→ Vector DB ──→ RAG Agent
```

### 2. Multi-Agent Swarm

The system is not a monolithic application but a coordinated swarm of specialized agents:

- **Processor Agent**: Data ingestion specialist
- **Orchestrator Agent**: Query coordinator
- **Detective Agent**: SQL expert
- **Interrogator Agent**: Semantic search expert
- **Link Analyzer**: Cross-reference specialist

### 3. Production-Ready from Day One

By using **SQLAlchemy** as the database abstraction layer, the prototype code is already production-ready. Migration to PostgreSQL requires only changing the connection string.

## Detailed Component Architecture

### Component 1: Processor Agent (`ingest_data.py`)

**Purpose**: Offline data ingestion into dual databases

**Process Flow**:
```
1. Accept UFDR folder/ZIP path
2. Extract if ZIP
3. Identify files by name/extension
4. For each structured file (CSV):
   - Parse with Pandas
   - Clean column names
   - Convert datatypes
   - Insert into SQL via SQLAlchemy
5. For each unstructured file (TXT):
   - Read content
   - Chunk into 500-word segments
   - Generate embeddings
   - Store in ChromaDB
6. Return case_id
```

**Key Design Decisions**:
- Uses `SQLAlchemy` for database abstraction (enables SQLite → PostgreSQL migration)
- Chunks text with 50-word overlap for context preservation
- Robust error handling (skips bad files, continues processing)
- Transaction-based inserts for data integrity

### Component 2: QueryAnalyzer (`agent_core.py`)

**Purpose**: Execute queries using specialized tools

**Architecture**:
```
QueryAnalyzer
    │
    ├─── Detective Tool (Text-to-SQL)
    │    │
    │    ├─── Get database schema
    │    ├─── Generate SQL with LLM
    │    ├─── Execute query
    │    └─── Return DataFrame
    │
    ├─── Interrogator Tool (RAG)
    │    │
    │    ├─── Perform semantic search
    │    ├─── Retrieve top-k documents
    │    ├─── Build context
    │    ├─── Generate answer with LLM
    │    └─── Return answer + sources
    │
    └─── Link Analyzer
         │
         ├─── Extract entities from SQL results
         ├─── Check mentions in RAG answer
         └─── Return cross-references
```

**Key Design Decisions**:
- **Detective Tool**: Generates SQL dynamically based on schema
- **Interrogator Tool**: Searches all collections for comprehensive results
- **Link Analyzer**: Deterministic logic, not AI inference
- Returns structured dictionaries for easy UI rendering

### Component 3: Orchestrator (`app.py`)

**Purpose**: Central nervous system that coordinates all components

**Process Flow**:
```
1. Receive user query from UI
2. Analyze query intent:
   - Contains SQL keywords? (count, filter, after, etc.)
   - Contains RAG keywords? (discuss, mention, explain, etc.)
   - If unclear, use both tools
3. Delegate to QueryAnalyzer
4. Receive results:
   - Detective results (if SQL used)
   - Interrogator results (if RAG used)
   - Link analysis (if both used)
5. Format and return to UI
```

**Key Design Decisions**:
- Intent analysis uses keyword matching (fast, predictable)
- Can invoke one or both tools based on query
- Maintains session state for multi-turn conversations
- Handles errors gracefully with user-friendly messages

### Component 4: User Interface (`app.py` - Streamlit)

**Purpose**: Provide intuitive web interface for non-technical users

**UI Components**:

1. **Sidebar**:
   - UFDR file upload
   - Sample case loading
   - System information
   - Architecture explanation

2. **Main Area**:
   - Query input box
   - Example queries
   - Results display
   - Chat history

3. **Results Display**:
   - Intent analysis (which tools used)
   - Detective results (SQL + table)
   - Interrogator results (answer + sources)
   - Link analysis (cross-references)
   - Auto-generated visualizations

**Key Design Decisions**:
- Session state for persistence
- Expandable sections for clean UI
- Auto-visualization based on data types
- Source citations for RAG answers

## Data Flow Diagrams

### Ingestion Flow

```
┌─────────────┐
│ UFDR Files  │
│ (ZIP/Folder)│
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Extract & Parse │
└──────┬──────────┘
       │
       ├────────────────────┬─────────────────────┐
       ▼                    ▼                     ▼
┌──────────────┐   ┌──────────────┐    ┌──────────────┐
│ CallLogs.csv │   │ Contacts.csv │    │ WhatsApp.txt │
│ SMS.csv      │   │ Bank.csv     │    │ Notes.txt    │
└──────┬───────┘   └──────┬───────┘    └──────┬───────┘
       │                  │                     │
       │ Structured       │ Structured          │ Unstructured
       ▼                  ▼                     ▼
┌────────────────────────────┐     ┌───────────────────┐
│    SQL Database            │     │  Vector Database  │
│    (SQLite/PostgreSQL)     │     │  (ChromaDB)       │
└────────────────────────────┘     └───────────────────┘
```

### Query Flow

```
┌──────────────┐
│ User Query   │
│ "Show calls  │
│ after 10 PM" │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  Orchestrator    │
│  Intent Analysis │
└──────┬───────────┘
       │
       ├─── SQL Keywords? ──→ YES
       └─── RAG Keywords? ──→ NO
       │
       ▼
┌──────────────────┐
│ Detective Tool   │
│ Generate SQL     │
└──────┬───────────┘
       │
       │ SQL: SELECT * FROM calllogs
       │      WHERE time > '22:00:00'
       ▼
┌────────────────────────────┐
│    SQL Database            │
│    Execute Query           │
└──────┬─────────────────────┘
       │
       │ DataFrame (50 rows)
       ▼
┌──────────────────┐
│ Format Results   │
│ Generate Charts  │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Display in UI    │
└──────────────────┘
```

## Database Design

### SQL Database Schema

Tables are created dynamically based on CSV file structure. Example tables:

#### calllogs
```sql
CREATE TABLE calllogs (
    timestamp DATETIME,
    caller VARCHAR,
    receiver VARCHAR,
    duration INTEGER,
    type VARCHAR,
    location VARCHAR,
    cell_tower_id VARCHAR
);
```

#### contacts
```sql
CREATE TABLE contacts (
    name VARCHAR,
    phone VARCHAR,
    email VARCHAR,
    relation VARCHAR,
    notes TEXT,
    last_contact DATETIME
);
```

**Indexing Strategy** (Production):
```sql
CREATE INDEX idx_calllogs_timestamp ON calllogs(timestamp);
CREATE INDEX idx_calllogs_caller ON calllogs(caller);
CREATE INDEX idx_contacts_phone ON contacts(phone);
CREATE INDEX idx_bank_transactions_amount ON bank_transactions(amount_inr);
```

### Vector Database Schema

**Collections**: One per case (e.g., `ufdr_20251007_143022`)

**Document Structure**:
```json
{
    "document": "chunk of text (500 words)",
    "metadata": {
        "source": "WhatsApp_Chats.txt",
        "chunk_id": 0,
        "case_id": "20251007_143022"
    },
    "embedding": [0.123, 0.456, ...],  // Auto-generated
    "id": "WhatsApp_Chats.txt_0"
}
```

## AI/LLM Integration

### Model: Google Gemini Pro

**Why Gemini?**
- ✅ Free tier available
- ✅ Large context window (32k tokens)
- ✅ Fast inference
- ✅ Good at both code generation (SQL) and text generation (answers)
- ✅ Multimodal capabilities (future expansion)

### LLM Usage Patterns

#### 1. Text-to-SQL Generation

**Prompt Template**:
```
You are a SQL expert for forensic data analysis.

DATABASE SCHEMA:
{schema_info}

User Question: {question}

Generate a valid SQL query to answer this question.
Return ONLY the SQL query without explanation.

SQL Query:
```

**Temperature**: 0.1 (deterministic)
**Max Tokens**: 500

#### 2. RAG Answer Generation

**Prompt Template**:
```
You are a forensic analyst reviewing evidence.

Context from Evidence Files:
{retrieved_documents}

User Question: {question}

Based ONLY on the evidence above, answer thoroughly.
Cite specific sources when possible.

Answer:
```

**Temperature**: 0.3 (slightly creative)
**Max Tokens**: 1000

## Performance Optimization

### Query Optimization

1. **SQL Queries**:
   - Use indexes on frequently queried columns
   - Limit result sets with pagination
   - Cache schema information

2. **Vector Searches**:
   - Limit to top-k results (k=5)
   - Pre-filter by case_id when possible
   - Use HNSW indexing for large datasets

3. **LLM Calls**:
   - Minimize context length
   - Cache common queries
   - Batch similar queries

### Scalability Considerations

**Current (Prototype)**:
- Single SQLite file
- Local ChromaDB
- Single-user Streamlit
- LLM rate limits: ~60 requests/minute

**Production (PostgreSQL)**:
- Distributed SQL database
- Remote ChromaDB instance
- Multi-user with session management
- Increased LLM quotas

## Security Architecture

### Data Security

1. **At Rest**:
   - SQLite file permissions (chmod 600)
   - ChromaDB directory permissions
   - Encrypted .env file

2. **In Transit**:
   - HTTPS for production deployments
   - API key transmitted securely
   - No sensitive data in logs

### Access Control

**Current (Prototype)**:
- Local-only access
- No authentication

**Production**:
- Role-based access control (RBAC)
- User authentication (OAuth/SSO)
- Audit logging
- Session management

## Error Handling Strategy

### Graceful Degradation

```python
try:
    # Execute SQL query
    results = execute_sql(query)
except Exception as e:
    # Log error
    logger.error(f"SQL error: {e}")
    # Return empty results with error message
    return {'success': False, 'error': str(e), 'data': []}
```

### User-Friendly Messages

- Technical errors → Simple explanations
- Logs detailed errors → Shows summary to user
- Suggests corrective actions

## Testing Strategy

### Unit Tests (Planned)

```python
# test_detective_tool.py
def test_sql_generation():
    tool = DetectiveTool(db_url, llm)
    result = tool.query("How many calls?")
    assert 'SELECT COUNT' in result['sql_query']

# test_interrogator_tool.py
def test_semantic_search():
    tool = InterrogatorTool(chroma_dir, llm)
    result = tool.query("What did suspects discuss?")
    assert result['success'] == True
    assert len(result['sources']) > 0
```

### Integration Tests

```python
def test_end_to_end_query():
    orchestrator = Orchestrator()
    result = orchestrator.handle_query("Show all calls")
    assert result['status'] == 'success'
```

## Deployment Architecture

### Docker Deployment

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/drishti
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=drishti
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

### Cloud Deployment Options

1. **AWS**:
   - ECS/Fargate for containers
   - RDS for PostgreSQL
   - S3 for file storage

2. **Google Cloud**:
   - Cloud Run for containers
   - Cloud SQL for PostgreSQL
   - Cloud Storage for files

3. **Azure**:
   - Container Instances
   - Azure Database for PostgreSQL
   - Blob Storage

## Future Enhancements

### Phase 2 Features

1. **Advanced Visualizations**:
   - Network graphs for link analysis
   - Timeline visualizations
   - Geographic mapping

2. **Multi-Case Management**:
   - Compare across cases
   - Cross-case link analysis
   - Case templates

3. **Export Capabilities**:
   - PDF reports
   - DOCX summaries
   - CSV exports

### Phase 3 Features

1. **Machine Learning**:
   - Pattern detection
   - Anomaly detection
   - Predictive analytics

2. **Real-Time Collaboration**:
   - Multi-user access
   - Shared annotations
   - Team chat

3. **Advanced Analytics**:
   - Social network analysis
   - Behavioral profiling
   - Risk scoring

## Conclusion

Project Drishti's architecture is designed for:
- ✅ **Modularity**: Each component is independent
- ✅ **Scalability**: Prototype → Production path is clear
- ✅ **Maintainability**: Clean separation of concerns
- ✅ **Extensibility**: Easy to add new features
- ✅ **Production-Ready**: SQLAlchemy abstraction enables seamless database migration

The Hybrid Intelligence approach ensures optimal handling of diverse data types, making it a powerful tool for forensic investigation.
