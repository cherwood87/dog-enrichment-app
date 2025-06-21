#!/bin/bash

# Setup script for bulk PDF import
echo "🐕 Setting up Bulk PDF Importer for Dog Enrichment Activities"
echo "============================================================="

# Check if we're in the right directory
if [ ! -f "enrichment_database.py" ]; then
    echo "❌ Please run this script from the dog-enrichment-app directory"
    exit 1
fi

echo "📦 Installing required Python packages..."

# Install required packages
pip3 install PyPDF2 pdfplumber

if [ $? -eq 0 ]; then
    echo "✅ Packages installed successfully!"
    echo ""
    echo "🚀 Ready to import PDFs!"
    echo ""
    echo "To start importing your PDFs, run:"
    echo "python3 bulk_pdf_importer.py"
    echo ""
    echo "This will:"
    echo "• Find all your enrichment PDFs"
    echo "• Extract activities automatically"
    echo "• Match the format and style of existing activities"
    echo "• Add them to your database"
else
    echo "❌ Error installing packages. You might need to run:"
    echo "brew install python3"
    echo "or check your Python installation"
fi
