# UFDR Sample Reports Collection
## Universal Forensic Extraction Device Report - Simulated Data

**⚠️ DISCLAIMER: All data in this collection is completely fictional and created for software development and testing purposes only. Any resemblance to real persons, places, or events is purely coincidental.**

---

## 📁 Collection Overview

This directory contains realistic, interconnected UFDR (Universal Forensic Extraction Device Report) datasets designed for testing and developing forensic analysis systems. Each case represents a different type of criminal investigation with comprehensive digital evidence across multiple data types.

### Dataset Statistics
- **Total Cases**: 3
- **Total Files**: 29
- **File Types**: CSV, TXT (structured and unstructured data)
- **Time Period**: September 2025
- **Geographic Coverage**: Multiple cities across India

---

## 🗂️ Case Files

### Case 001: Cyber Fraud Ring
**Location**: Bangalore, Hyderabad, Mumbai, Pune, Chennai  
**Suspects**: 4 primary suspects  
**Crime Type**: Phishing operations, money laundering  
**Estimated Losses**: ₹4+ lakh daily  
**Files**: 11

**Key Evidence**:
- Organized phishing operations targeting senior citizens
- Multi-city call center operations
- Cryptocurrency money laundering
- Encrypted communication channels
- Anti-forensics tools usage

**Interconnected Data**:
- Phone numbers cross-referenced across CallLogs, SMS, WhatsApp
- Financial transactions linked to specific communications
- Location data correlates with meeting patterns
- Browser history reveals dark web activities
- App usage shows encryption and VPN tools

---

### Case 002: Drug Trafficking Network
**Location**: Goa, Mumbai, Delhi, Pune, Kolkata  
**Suspects**: 6 primary suspects + 1 enforcer  
**Crime Type**: Drug production, distribution, cross-border trafficking  
**Estimated Revenue**: ₹45 lakh weekly  
**Files**: 9

**Key Evidence**:
- Large-scale drug production facility in Goa
- International supply chain (Nepal, Malaysia, Dubai)
- Pharmaceutical front for precursor chemicals
- Violent elimination of competition
- Customs bribery and port operations

**Interconnected Data**:
- Call patterns show coordination across 5 cities
- Payment flows trace production-to-distribution chain
- Location data reveals secret lab and meeting points
- WhatsApp group contains operational details
- Browser history shows dark web marketplace activity

---

### Case 003: Terrorism Network
**Location**: Srinagar, Kashmir Border, Jammu, Delhi, Mumbai  
**Suspects**: 7 operatives + foreign handler  
**Crime Type**: Planned terror attacks, cross-border coordination  
**Threat Level**: CRITICAL - IMMINENT  
**Files**: 9

**Key Evidence**:
- Coordinated multi-city terror attacks planned for October 2, 2025
- 30 kg RDX with military-grade detonators
- Vehicle-Borne IEDs prepared
- Cross-border weapons smuggling
- Hawala funding network (₹50 lakh from Pakistan)
- Martyrdom videos recorded
- Multiple high-profile targets identified

**Interconnected Data**:
- Encrypted communications reveal detailed attack plans
- Financial trail traces hawala and cryptocurrency funding
- Location history shows cross-border movements
- Device analysis reveals military-grade encryption
- Timeline shows escalating operational tempo

---

## 📊 File Types Included

Each case folder contains a combination of the following evidence types:

### Structured Data (CSV Files)
1. **CallLogs.csv** - Phone call records with timestamps, participants, duration, location
2. **Contacts.csv** - Contact list with names, numbers, emails, relationship notes
3. **SMS_Messages.csv** - Text message records with timestamps and content
4. **Location_History.csv** - GPS and cell tower location data
5. **Browser_History.csv** - Web browsing history with URLs and visit counts
6. **App_Usage.csv** - Application usage statistics and permissions
7. **Email_Records.csv** - Email communications with metadata
8. **Bank_Transactions.csv** - Financial transaction records

### Unstructured Data (TXT Files)
1. **WhatsApp_Chats.txt** - Conversational chat exports with context
2. **Device_Info.txt** - Detailed device specifications and forensic notes
3. **Notes.txt** - Investigative notes, case summaries, evidence markers

---

## 🔗 Data Interconnections

The datasets are designed to demonstrate cross-referencing capabilities:

### Within Each Case
- Phone numbers appear consistently across CallLogs, SMS, Contacts, WhatsApp
- Timestamps correlate across different evidence types
- Financial transactions align with communication patterns
- Location data matches with meeting times and call records
- App usage reflects communication channel preferences

### Investigative Insights Available
- **Network Analysis**: Identify key players through call pattern analysis
- **Timeline Reconstruction**: Build event sequences from multiple data sources
- **Financial Flows**: Trace money movement through transaction records
- **Geolocation Correlation**: Map movements and meeting locations
- **Communication Analysis**: Understand operational structure from messages
- **Link Discovery**: Find hidden connections between suspects and activities

---

## 🎯 Use Cases

These datasets are designed for:

1. **AI/ML Training**: Train natural language models for forensic analysis
2. **Software Testing**: Test UFDR analysis tools and systems
3. **Algorithm Development**: Develop link analysis and pattern detection algorithms
4. **Educational Purposes**: Train law enforcement and investigators
5. **Prototype Development**: Build proof-of-concept forensic systems
6. **Query Testing**: Test natural language query systems (e.g., Project Drishti)

---

## 🔍 Sample Queries for Testing

### Simple Queries
- "Show all calls after 10 PM"
- "Find contacts without saved names"
- "List all financial transactions over ₹1 lakh"
- "Show WhatsApp messages mentioning 'payment'"

### Complex Cross-Reference Queries
- "Find all communications between suspects who met in Mumbai"
- "Show financial transactions that occurred within 2 hours of specific calls"
- "Identify phone numbers that appear in contacts but never called"
- "Find locations visited by multiple suspects on the same day"

### Advanced Link Analysis
- "Trace the money flow from source to final recipient"
- "Build a network graph of all suspects and their connections"
- "Identify suspicious patterns in communication timing"
- "Find encrypted app usage correlated with high-value transactions"

---

## 📋 Data Schema

### CallLogs.csv
```
Timestamp, Caller, Receiver, Duration, Type, Location, Cell_Tower_ID
```

### Contacts.csv
```
Name, Phone, Email, Relation, Notes, Last_Contact
```

### SMS_Messages.csv
```
Timestamp, Sender, Receiver, Message, Location, Status
```

### Location_History.csv
```
Timestamp, Latitude, Longitude, Location, Accuracy, Source, Activity
```

### Bank_Transactions.csv
```
Timestamp, Account_Number, Amount_INR, Type, Beneficiary, Bank/Method, Notes
```

---

## ⚠️ Important Notes

1. **Fictional Data**: All names, numbers, locations, and events are completely fictional
2. **Educational Purpose**: Designed exclusively for software development and training
3. **No Real Cases**: Does not represent or reference any actual investigations
4. **Privacy Compliant**: Contains no real personal or sensitive information
5. **Testing Only**: Should not be used for any operational law enforcement purposes

---

## 🚀 Getting Started

### For Developers
```python
import pandas as pd

# Load structured data
call_logs = pd.read_csv('case_001_cyber_fraud_ring/CallLogs.csv')
contacts = pd.read_csv('case_001_cyber_fraud_ring/Contacts.csv')

# Load unstructured data
with open('case_001_cyber_fraud_ring/WhatsApp_Chats.txt', 'r') as f:
    chats = f.read()
```

### For Testing Query Systems
Try these test queries:
1. "Who did Amit Patel call most frequently?"
2. "Show me all messages mentioning money or payment"
3. "Find suspicious late-night communications"
4. "Trace the financial transactions between suspects"

---

## 📈 Future Enhancements

Potential additions to this dataset collection:
- [ ] More case types (kidnapping, corporate espionage, etc.)
- [ ] Social media data (Facebook, Instagram, Twitter)
- [ ] Photos and video metadata
- [ ] Audio recording transcripts
- [ ] Cloud storage forensics
- [ ] IoT device data
- [ ] Cryptocurrency wallet analysis

---

## 📝 Version History

**v1.0.0** (October 2025)
- Initial release with 3 comprehensive cases
- 29 interconnected evidence files
- Multiple data types (structured and unstructured)
- Cross-case referencing capabilities

---

## 🤝 Contributing

If you'd like to add more realistic case scenarios or improve existing datasets:
1. Maintain data consistency and cross-references
2. Keep all data completely fictional
3. Ensure realistic patterns and timelines
4. Document interconnections clearly

---

## 📧 Contact

For questions about this dataset collection:
- Project: Drishti (Insight) - Conversational AI for UFDR Analysis
- Repository: https://github.com/Pswaikar1742/Drishti

---

**Last Updated**: October 7, 2025  
**Dataset Version**: 1.0.0  
**Total Evidence Files**: 29  
**Total Cases**: 3
