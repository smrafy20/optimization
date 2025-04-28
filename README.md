# PDF Text Extractor

A Flask web application for extracting text from PDF files using various methods, including OCR and direct text extraction, with special support for Bangla language.

## Features

- **NO OCR Based Bangla**: Extract text from Bijoy-encoded Bangla PDF files without using OCR
- **NO OCR Based English**: Extract text from English PDF files without using OCR
- **OCR Based Bangla**: Use OCR to extract Bangla text from image-based PDFs
- **OCR Based Multi-Language**: Automatically detect and extract text from PDFs containing both Bangla and English
- **OCR Split Format**: Split PDF pages into left and right halves before OCR, ideal for MCQ PDFs

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
   - In `OCR_bn_raw.py`, `OCR_multi.py`, and `OCR_multi_split.py`, update the Tesseract and Poppler paths according to your installation.

## Usage

1. Start the Flask application:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Upload a PDF file, select the processing method, and click "Process PDF"

4. The processed text file will be available for download

## Processing Methods

- **NO OCR Based Bangla**: Best for Bijoy encoded Bangla PDF files with selectable text
- **NO OCR Based English**: Best for English PDF files with selectable text
- **OCR Based Bangla**: Good for image-based Bangla PDFs, especially CQ files
- **OCR Based Multi-Language**: Good for mixed content PDFs with both Bangla and English
- **OCR Split Format**: Best for MCQ PDFs with split page format

## Output Formats

- **TXT**: Plain text output (available for all methods)
- **DOCX**: Microsoft Word document.

## Notes

- The NO OCR methods are faster but require PDFs with selectable text
- The OCR methods work with any PDF, even scanned documents, but are slower
- The OCR Split method is specifically designed for MCQ PDFs with questions on both left and right sides
- For Bangla OCR, make sure the Tesseract Bengali language pack is installed 
