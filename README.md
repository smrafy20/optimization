# PDF Text Extractor

A Flask web application for extracting text from PDF files using automatic language detection, with special support for Bangla and English mixed content.

## Features

- **NO OCR**: Direct text extraction with automatic language detection for both Bangla and English
- **OCR Based**: Image-based text extraction with automatic language detection for both Bangla and English
- Supports both TXT and DOCX output formats
- Handles mixed language content seamlessly
- Fast and accurate processing

## Requirements

- Python 3.7+
- Tesseract OCR (for OCR-based methods)
- Poppler (for PDF to image conversion)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pdf-text-extractor
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install Tesseract OCR:
   - **Windows**: Download and install from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - **Mac**: `brew install tesseract tesseract-lang`
   - **Linux**: `sudo apt-get install tesseract-ocr tesseract-ocr-ben` (include Bengali language pack)

4. Install Poppler:
   - **Windows**: Download from [poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
   - **Mac**: `brew install poppler`
   - **Linux**: `sudo apt-get install poppler-utils`

5. Update the paths in the code if necessary:
   - In `OCR_unified.py`, update the Tesseract and Poppler paths according to your installation.

## Usage

1. Start the Flask application:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Upload a PDF file, select the processing method (NO OCR or OCR), and click "Process PDF"

4. The processed file will be automatically downloaded

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
