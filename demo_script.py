#!/usr/bin/env python3
"""
🎯 Project Drishti Demo Script
============================

This script demonstrates key features of Project Drishti for screenshot
and documentation purposes. Run this to see the system in action.

Usage:
    python demo_script.py
    
Requirements:
    - Streamlit app running on localhost:8503
    - Sample data already ingested via ingest_data.py
    - Virtual environment activated with all dependencies
"""

import requests
import time
import json
from datetime import datetime

class DrishtiDemo:
    def __init__(self, base_url="http://localhost:8503"):
        self.base_url = base_url
        self.demo_queries = [
            # SQL Detective Tool Demos
            {
                "type": "SQL",
                "query": "Show me all calls longer than 5 minutes between January 1-15, 2024",
                "description": "Call duration analysis for timeline reconstruction"
            },
            {
                "type": "SQL", 
                "query": "Find all transactions above $10,000 in the last 30 days",
                "description": "High-value financial transaction detection"
            },
            {
                "type": "SQL",
                "query": "List all contacts who called the same number as the suspect",
                "description": "Communication network mapping"
            },
            
            # RAG Interrogator Tool Demos
            {
                "type": "RAG",
                "query": "Find mentions of suspicious meetings or planned activities",
                "description": "Semantic analysis of WhatsApp chat content"
            },
            {
                "type": "RAG",
                "query": "Look for discussions about money, payments, or financial arrangements",
                "description": "Financial evidence in unstructured communications"
            },
            {
                "type": "RAG",
                "query": "Search for location references and meeting coordinates",
                "description": "Location intelligence from text messages"
            },
            
            # Cross-Reference Analysis
            {
                "type": "HYBRID",
                "query": "Cross-reference: Who had calls during the times mentioned in WhatsApp chats about meetings?",
                "description": "Hybrid intelligence connecting structured and unstructured data"
            }
        ]
    
    def print_banner(self):
        """Print demo banner"""
        print("=" * 70)
        print("🚀 PROJECT DRISHTI v1.0 - AI FORENSIC ANALYSIS DEMO")
        print("=" * 70)
        print()
        print("🎯 This demo showcases key forensic investigation capabilities:")
        print("   • SQL Detective Tool - Natural language to SQL conversion")
        print("   • RAG Interrogator Tool - Semantic document analysis")  
        print("   • Hybrid Intelligence - Cross-referencing capabilities")
        print("   • Forensic Visualizations - Timeline and pattern analysis")
        print()
    
    def check_app_status(self):
        """Check if Streamlit app is running"""
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code == 200:
                print("✅ Streamlit app is running at", self.base_url)
                return True
            else:
                print("❌ Streamlit app not responding correctly")
                return False
        except requests.exceptions.RequestException:
            print("❌ Cannot connect to Streamlit app at", self.base_url)
            print("📋 Make sure to run: python -m streamlit run app.py --server.port 8503")
            return False
    
    def demonstrate_queries(self):
        """Demonstrate sample forensic queries"""
        print("\n🔍 SAMPLE FORENSIC INVESTIGATION QUERIES")
        print("=" * 50)
        
        for i, demo in enumerate(self.demo_queries, 1):
            print(f"\n📋 Demo {i}: {demo['description']}")
            print(f"🔧 Tool: {demo['type']} {'Detective' if demo['type'] == 'SQL' else 'Interrogator' if demo['type'] == 'RAG' else 'Intelligence'}")
            print(f"💬 Query: \"{demo['query']}\"")
            print("⏱️  Processing... (Enter this query in the Streamlit interface)")
            time.sleep(2)
    
    def show_visualization_guide(self):
        """Show what visualizations to look for"""
        print("\n📊 FORENSIC VISUALIZATIONS TO CAPTURE")
        print("=" * 45)
        print("🎯 After running queries, look for these elements:")
        print("   • 📈 Timeline Charts - Communication patterns over time")
        print("   • 🔗 Network Graphs - Relationship mapping between contacts")
        print("   • 📊 Pattern Analysis - Frequency and duration insights")
        print("   • 📤 Export Buttons - CSV download for court evidence")
        print("   • 🎨 Interactive Plots - Hover details and zoom capabilities")
    
    def show_screenshot_instructions(self):
        """Show instructions for capturing screenshots"""
        print("\n📸 SCREENSHOT CAPTURE INSTRUCTIONS")
        print("=" * 40)
        print("1. 🖥️  Main Dashboard:")
        print("   - Open http://localhost:8503")
        print("   - Show both tool options (SQL Detective + RAG Interrogator)")
        print("   - Capture clean interface before entering queries")
        
        print("\n2. 🔍 SQL Detective Demo:")
        print("   - Enter: 'Show me all calls longer than 5 minutes'")
        print("   - Capture the SQL generation and results table")
        print("   - Highlight the natural language → SQL conversion")
        
        print("\n3. 💬 RAG Analysis Demo:")
        print("   - Enter: 'Find mentions of suspicious meetings'")
        print("   - Capture document chunks and relevance scores")
        print("   - Show semantic search highlighting")
        
        print("\n4. 📊 Visualization Screenshot:")
        print("   - Scroll to charts after any successful query")
        print("   - Capture timeline, patterns, and export buttons")
        print("   - Show interactive elements and hover details")
    
    def show_sample_results(self):
        """Show expected sample results"""
        print("\n🎯 EXPECTED DEMO RESULTS")
        print("=" * 30)
        print("📞 Call Analysis Results:")
        print("   • 15+ call records longer than 5 minutes")
        print("   • Suspect communication patterns identified")
        print("   • Timeline correlation with other evidence")
        
        print("\n💰 Transaction Analysis:")
        print("   • 8+ high-value transactions detected")
        print("   • Money flow patterns visualized")
        print("   • Suspicious timing correlations")
        
        print("\n💬 Chat Analysis:")  
        print("   • 12+ relevant document chunks found")
        print("   • Meeting references extracted")
        print("   • Location and time intelligence")
    
    def run_demo(self):
        """Run the complete demo"""
        self.print_banner()
        
        if not self.check_app_status():
            return
            
        print("\n⏱️  Starting demo in 3 seconds...")
        time.sleep(3)
        
        self.demonstrate_queries()
        self.show_visualization_guide()
        self.show_screenshot_instructions()
        self.show_sample_results()
        
        print("\n" + "=" * 70)
        print("🎉 DEMO COMPLETE - Ready for Screenshots!")
        print("=" * 70)
        print("📋 Next Steps:")
        print("   1. Run the sample queries in the Streamlit interface")
        print("   2. Capture screenshots of results and visualizations")
        print("   3. Export sample CSV reports for documentation")
        print("   4. Update PR with actual screenshot URLs")
        print("\n🚀 Project Drishti is ready for forensic investigations!")

if __name__ == "__main__":
    demo = DrishtiDemo()
    demo.run_demo()