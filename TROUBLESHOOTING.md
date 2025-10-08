# Troubleshooting Guide - Project Drishti

## Issue: Pydantic v2 Compatibility Error

### Problem Description
```
PydanticUserError: The `__modify_schema__` method is not supported in Pydantic v2. 
Use `__get_pydantic_json_schema__` instead in class `SecretStr`.
```

This error occurred when trying to run the application with incompatible package versions.

### Root Cause
- The system had both global Python packages (in `~/.local/lib/python3.13/site-packages`) and virtual environment packages
- Older versions of `langchain-google-genai` and `langchain-core` were not compatible with Pydantic v2
- The virtual environment needed proper dependency installation

### Solution

#### 1. Use Virtual Environment Properly
Always run Python commands using the virtual environment's Python executable:

```bash
# Correct way to run Streamlit
/home/psw/Projects/Drishti/venv/bin/python3 -m streamlit run app.py

# NOT: streamlit run app.py (uses global packages)
# NOT: python3 app.py (may use global packages)
```

#### 2. Updated Package Versions
Updated `requirements.txt` with compatible versions:

```txt
# Core Framework
pydantic==2.9.2
pydantic-settings==2.5.2

# AI/LLM Framework - CRITICAL VERSIONS
langchain==0.3.27
langchain-google-genai==2.0.6
google-generativeai==0.8.3
langchain-core==0.3.78  # Must be >= 0.3.75 for compatibility
langchain-community==0.3.30

# Data Processing
numpy>=1.26.0  # Changed from pinned version to allow pre-built wheels
```

#### 3. Installation Steps for Python 3.13

For Python 3.13, some packages like `numpy 1.26.4` require C++ compiler which may not be available. Use flexible version ranges:

```bash
# Step 1: Configure Python environment
cd /home/psw/Projects/Drishti

# Step 2: Install numpy with pre-built wheels
/home/psw/Projects/Drishti/venv/bin/pip install --only-binary=:all: numpy

# Step 3: Install all requirements
/home/psw/Projects/Drishti/venv/bin/pip install -r requirements.txt
```

#### 4. Missing Dependencies
If you encounter missing dependency errors, install them manually:

```bash
# Core Streamlit dependencies
/home/psw/Projects/Drishti/venv/bin/pip install blinker click altair gitpython pillow pyarrow pydeck toml tornado

# ChromaDB dependencies
/home/psw/Projects/Drishti/venv/bin/pip install bcrypt build importlib-resources mmh3 onnxruntime opentelemetry-api opentelemetry-exporter-otlp-proto-grpc opentelemetry-sdk overrides posthog pybase64 pypika rich tokenizers typer

# Other core dependencies
/home/psw/Projects/Drishti/venv/bin/pip install pytz tzdata contourpy cycler fonttools kiwisolver starlette greenlet aiohttp dataclasses-json httpx-sse langchain-text-splitters mako et-xmlfile
```

### Verification

After installation, verify the app starts correctly:

```bash
cd /home/psw/Projects/Drishti
/home/psw/Projects/Drishti/venv/bin/python3 -m streamlit run app.py
```

You should see:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8502
Network URL: http://10.67.4.165:8502

...
INFO - Detective Tool (Text-to-SQL) initialized
INFO - Interrogator Tool (RAG) initialized
INFO - QueryAnalyzer initialized with Detective and Interrogator tools
INFO - UFDR Processor initialized
INFO - Orchestrator initialized
```

### Common Warnings (Safe to Ignore)

These warnings are harmless and don't affect functionality:

1. **ALTS Credentials Warning**:
   ```
   WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
   E0000 00:00:xxx ALTS creds ignored. Not running on GCP and untrusted ALTS is not enabled.
   ```
   - This is from Google's gRPC library
   - Only relevant if running on Google Cloud Platform
   - Safe to ignore for local development

2. **ChromaDB Telemetry Error**:
   ```
   chromadb.telemetry.product.posthog - ERROR - Failed to send telemetry event ClientStartEvent: 
   capture() takes 1 positional argument but 3 were given
   ```
   - ChromaDB analytics issue with newer PostHog version
   - Doesn't affect database functionality
   - Safe to ignore

### File Upload Feature

The application already includes a complete UFDR file upload feature:

**Location**: Sidebar in the Streamlit UI

**Features**:
1. **ZIP File Upload**: Upload UFDR reports as ZIP files
2. **Case ID**: Optional custom case ID (auto-generated if not provided)
3. **Sample Cases**: Quick-load buttons for pre-existing sample cases
4. **Processing**: Automatic ingestion into SQL and Vector databases

**Usage**:
1. Open the app: http://localhost:8502
2. Look for "📁 UFDR Upload" section in the sidebar
3. Click "Choose UFDR ZIP file" and select your ZIP file
4. Optionally enter a Case ID
5. Click "🚀 Process UFDR"
6. Wait for "✅ Successfully processed case..." message
7. Start querying your data!

### Quick Setup Script

For future installations, use this script:

```bash
#!/bin/bash
# setup_venv.sh - Complete setup script

cd /home/psw/Projects/Drishti

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install numpy first (with binary wheels only)
pip install --only-binary=:all: numpy

# Install all requirements
pip install -r requirements.txt

# Run the application
python3 -m streamlit run app.py
```

Save as `setup_venv.sh`, make executable:
```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

### Alternative: Using Conda

If you continue to have issues with pip, consider using Conda:

```bash
# Create conda environment
conda create -n drishti python=3.10
conda activate drishti

# Install packages
conda install -c conda-forge numpy pandas sqlalchemy streamlit
pip install -r requirements.txt

# Run
streamlit run app.py
```

Note: Python 3.10 is recommended for Conda as it has better package availability than 3.13.

## Other Common Issues

### Issue: ModuleNotFoundError

**Symptom**: `ModuleNotFoundError: No module named 'xxx'`

**Solution**: Install the missing module
```bash
/home/psw/Projects/Drishti/venv/bin/pip install <module_name>
```

### Issue: Google API Key Error

**Symptom**: `GOOGLE_API_KEY not found in environment variables!`

**Solution**: 
1. Edit `.env` file
2. Add your Google Gemini API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```
3. Get a free API key from: https://makersuite.google.com/app/apikey

### Issue: Database Locked

**Symptom**: `OperationalError: database is locked`

**Solution**: 
1. Close any other connections to `drishti.db`
2. Delete `drishti.db` and reingest data
3. For production, migrate to PostgreSQL (see README.md)

### Issue: Port Already in Use

**Symptom**: `Address already in use: http://localhost:8501`

**Solution**:
```bash
# Find and kill process using port 8501
lsof -ti:8501 | xargs kill -9

# Or use a different port
/home/psw/Projects/Drishti/venv/bin/python3 -m streamlit run app.py --server.port 8502
```

## Getting Help

If you encounter other issues:

1. Check the logs in the terminal for specific error messages
2. Verify all environment variables in `.env` are set correctly
3. Ensure you're using the virtual environment's Python
4. Try deleting `venv/` and reinstalling from scratch
5. Check GitHub Issues: https://github.com/Pswaikar1742/Drishti/issues

## Success Indicators

Your installation is successful when you see:

✅ Streamlit app opens in browser  
✅ No red error messages in sidebar  
✅ "No case loaded" warning (expected before uploading data)  
✅ Sample case buttons visible in sidebar  
✅ Query interface ready to use  

## Next Steps

Once the app is running:

1. **Load Sample Data**: Click "📂 Load Cyber Fraud Ring" in sidebar
2. **Try Example Queries**: Expand "💡 Example Queries" section
3. **Test Upload**: Upload your own UFDR ZIP file
4. **Explore Features**: Try Detective (SQL) and Interrogator (RAG) queries

---

**Last Updated**: October 7, 2025  
**Version**: 1.0  
**Python Version**: 3.13  
**Status**: ✅ Resolved
