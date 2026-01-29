# PDF Text Extractor - Multi-Method Conversion Tool

A comprehensive Flask-based web application that extracts text from PDF files using **three different processing methods**: No OCR, OCR-based, and GenAI-powered extraction.

## 🚀 Features

### Three Processing Methods:

#### 1. **No OCR Method** 
- Direct text extraction from text-based PDFs
- Auto-detects Bangla (with Bijoy conversion) and English
- Fast and accurate for digital PDFs with embedded text
- Best for: Clean PDFs with selectable text

#### 2. **OCR Method**
- Image-based text recognition using Tesseract
- Auto-detects and processes Bangla and English content
- Converts PDF pages to images and extracts text
- Best for: Scanned documents and image-based PDFs

#### 3. **GenAI Method** (NEW!)
- Powered by Google Gemini AI (gemini-2.0-flash-exp)
- High accuracy for complex layouts and mixed languages
- Intelligent text extraction with context understanding
- Best for: Complex documents, challenging layouts, mixed content
- **Requires: Google Gemini API Key**

## 📋 Features Overview

- ✅ **Multiple output formats**: TXT and DOCX
- ✅ **Auto language detection**: Automatically detects Bangla, English, or mixed content
- ✅ **Drag & drop file upload**: User-friendly interface
- ✅ **Real-time processing status**: Visual feedback during conversion
- ✅ **Responsive design**: Works on desktop and mobile
- ✅ **Error handling**: Graceful error messages and recovery

## 🛠️ Installation

### Prerequisites

1. **Python 3.8+**
2. **Tesseract OCR** (for OCR method)
   - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - Install to: `C:\Program Files\Tesseract-OCR\`
3. **Poppler** (for PDF to image conversion)
   - Windows: Download from [GitHub](https://github.com/oschwartz10612/poppler-windows/releases)
   - Extract to: `C:\Program Files\poppler-24.08.0\`
4. **Google Gemini API Key** (for GenAI method)
   - Get free API key from [Google AI Studio](https://ai.google.dev/)

### Setup Steps

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Tesseract Language Data**
   - Download Bengali language data: [ben.traineddata](https://github.com/tesseract-ocr/tessdata)
   - Place in: `C:\Program Files\Tesseract-OCR\tessdata\`

## 🚀 Usage

### Starting the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

### Using the Web Interface

1. **Upload a PDF file**
   - Drag & drop or click "Browse File"
   - Maximum file size: 16MB

2. **Select Processing Method**
   - **No OCR**: For text-based PDFs (fastest)
   - **OCR**: For scanned/image PDFs (moderate speed)
   - **GenAI**: For complex layouts (requires API key, most accurate)

3. **Enter API Key** (GenAI only)
   - Paste your Google Gemini API key when using GenAI method

4. **Choose Output Format**
   - TXT: Plain text file
   - DOCX: Microsoft Word document

5. **Click "Process PDF"**
   - Wait for processing to complete
   - Download will start automatically

## 🎯 When to Use Each Method

| Method | Use Case | Speed | Accuracy | Cost |
|--------|----------|-------|----------|------|
| **No OCR** | Digital PDFs with selectable text | ⚡ Fastest | ✅ High | Free |
| **OCR** | Scanned documents, images | ⏱️ Moderate | ✅ Good | Free |
| **GenAI** | Complex layouts, mixed languages | ⏱️ Moderate | ⭐ Excellent | Paid API |

## Processing Methods

- **NO OCR**: Direct text extraction with automatic language detection
  - Automatically detects Bangla (including Bijoy encoding) and English
  - Fast and accurate for text-based PDFs
  - Best for PDFs with selectable text

- **OCR Based**: Image-based extraction with automatic language detection
  - Automatically detects and processes Bangla and English content
  - Works with scanned documents and image-based PDFs
  - Slower but works with any PDF type

## Output Formats

- **TXT**: Plain text output (available for both methods)
- **DOCX**: Microsoft Word document (available for both methods)

## Notes

- The NO OCR method is faster but requires PDFs with selectable text
- The OCR method works with any PDF, even scanned documents, but is slower
- Both methods automatically detect language, no manual selection needed
- For Bangla OCR, make sure the Tesseract Bengali language pack is installed
- Mixed Bangla-English content is fully supported 
