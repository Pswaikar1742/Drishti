# 📸 Screenshots Guide for Project Drishti

## How to Capture Screenshots for Documentation

### 1. Main Dashboard Screenshot
- **URL**: http://localhost:8503
- **Focus**: Show both SQL Detective and RAG Interrogator tools
- **Filename**: `main-dashboard.png`
- **Resolution**: 1920x1080 recommended

### 2. SQL Detective Tool Demo
- **Action**: Enter query "Show me all calls longer than 5 minutes"
- **Focus**: Natural language input → SQL conversion → Results
- **Filename**: `sql-detective-demo.png`
- **Key Elements**: Query input, generated SQL, data table results

### 3. RAG Interrogator Analysis  
- **Action**: Enter "Find mentions of suspicious meetings in WhatsApp chats"
- **Focus**: Semantic search results with highlighted matches
- **Filename**: `rag-analysis-demo.png`
- **Key Elements**: Search query, document chunks, relevance scores

### 4. Forensic Visualizations
- **Action**: Scroll to visualization section after any query
- **Focus**: Timeline charts, pattern graphs, export buttons
- **Filename**: `forensic-visualizations.png`
- **Key Elements**: Charts, download buttons, data insights

### 5. Export Functionality
- **Action**: Click "Download Evidence Report" after analysis
- **Focus**: Export options and downloadable CSV files
- **Filename**: `export-functionality.png`
- **Key Elements**: Download buttons, file format options

## 📋 Screenshot Capture Checklist

### Before Capturing
- [ ] Streamlit app running on localhost:8503
- [ ] Sample data loaded (run `python ingest_data.py` if needed)
- [ ] Browser window maximized for best visibility
- [ ] Clear any previous query results for clean screenshots

### During Capture
- [ ] Use realistic forensic queries from QUESTIONS.md
- [ ] Capture full workflow: input → processing → results
- [ ] Include UI elements like buttons and menus
- [ ] Show data visualization charts clearly

### After Capture
- [ ] Optimize image size (recommended < 500KB each)
- [ ] Add descriptive filenames matching PR documentation
- [ ] Upload to GitHub repository or use image hosting
- [ ] Update PR description with actual image URLs

## 🎯 Key Areas to Highlight

### User Experience
- Clean, professional interface suitable for forensic investigators
- Natural language input that doesn't require SQL knowledge  
- Clear result presentation with actionable insights
- Export functionality for court-ready reports

### Technical Capabilities
- Real-time AI processing with Gemini 2.5 Pro
- Hybrid intelligence combining SQL and semantic search
- Rich visualizations for pattern recognition
- Professional data export formats

### Sample Data Context
- Use realistic forensic scenarios from the 4 sample cases
- Show variety: calls, messages, transactions, locations
- Demonstrate cross-referencing between different data types
- Highlight timeline and pattern analysis capabilities

---

**Note**: Replace placeholder image URLs in PR_DESCRIPTION.md with actual screenshots once captured and uploaded to GitHub repository or image hosting service.