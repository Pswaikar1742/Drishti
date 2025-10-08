# Project Drishti - Quick Reference Guide

## 🚀 One-Minute Setup

```bash
# Linux/Mac
chmod +x setup.sh
./setup.sh

# Windows
setup.bat
```

## 📋 Essential Commands

### Start Application
```bash
streamlit run app.py
```

### Ingest UFDR Data
```bash
# From folder
python ingest_data.py --path /path/to/ufdr_folder

# From ZIP
python ingest_data.py --path /path/to/ufdr.zip
```

### Test Components
```bash
# Test QueryAnalyzer
python agent_core.py

# Test with custom case ID
python ingest_data.py --path ./ufdr_sample_reports/case_001_cyber_fraud_ring --case-id TEST_001
```

## 🔑 API Key Setup

1. Get key: https://makersuite.google.com/app/apikey
2. Edit `.env` file
3. Add: `GOOGLE_API_KEY=your_key_here`

## 📊 Sample Queries

### SQL Queries (Structured Data)
- "How many calls after 10 PM?"
- "List contacts without names"
- "Show transactions over ₹1 lakh"

### RAG Queries (Unstructured Data)
- "What did suspects discuss?"
- "Summarize the notes"
- "Explain device findings"

### Complex Queries (Both)
- "Find communications + transactions"
- "Timeline with chat context"

## 🐛 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| API Key error | Add key to `.env` file |
| Module not found | `pip install -r requirements.txt` |
| Port in use | Use `--server.port=8502` |
| Database locked | Delete `drishti.db` and re-ingest |

## 🏗️ Architecture Overview

```
User Query
    ↓
Orchestrator (decides: SQL? RAG? Both?)
    ↓
├── Detective Tool (SQL) → SQLite → Results
└── Interrogator Tool (RAG) → ChromaDB → Answer
    ↓
Link Analyzer (cross-reference)
    ↓
UI Display (tables, charts, insights)
```

## 📁 File Structure

```
Drishti/
├── app.py              # Streamlit UI + Orchestrator
├── ingest_data.py      # Data processor
├── agent_core.py       # AI agents (Detective + Interrogator)
├── requirements.txt    # Dependencies
├── .env                # Configuration
└── ufdr_sample_reports/# Sample data
```

## 🔄 Prototype → Production

Change **ONE LINE** in `.env`:

```env
# Prototype (SQLite)
DATABASE_URL=sqlite:///./drishti.db

# Production (PostgreSQL)
DATABASE_URL=postgresql://user:pass@host:5432/db
```

**That's it!** No code changes needed.

## 📞 Need Help?

- 📖 Full docs: `README.md`
- 🐛 Issues: GitHub Issues
- 💬 Questions: GitHub Discussions

---

**Project Drishti** - *Insight through AI*
