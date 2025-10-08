#!/bin/bash

# Project Drishti - Quick Setup Script
# This script automates the setup process

set -e  # Exit on error

echo "=========================================="
echo "Project Drishti - Quick Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
echo ""
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file and add your GOOGLE_API_KEY"
    echo "   Get your API key from: https://makersuite.google.com/app/apikey"
    echo ""
else
    echo "✓ .env file already exists"
fi

# Create necessary directories
echo ""
echo "Creating necessary directories..."
mkdir -p uploads
mkdir -p temp_extractions

# Ingest sample data
echo ""
echo "Would you like to ingest sample data? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo ""
    echo "Ingesting sample case 1..."
    python ingest_data.py --path ./ufdr_sample_reports/case_001_cyber_fraud_ring
    
    echo ""
    echo "Ingesting sample case 2..."
    python ingest_data.py --path ./ufdr_sample_reports/case_002_drug_trafficking
    
    echo ""
    echo "Ingesting sample case 3..."
    python ingest_data.py --path ./ufdr_sample_reports/case_003_terrorism_network
fi

echo ""
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your GOOGLE_API_KEY"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run the application: streamlit run app.py"
echo ""
echo "Documentation: README.md"
echo "=========================================="
