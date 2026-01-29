import fitz  # PyMuPDF
import PyPDF2
import unicodeconverter
import os
from docx import Document
import re


def detect_language(text_sample):
    """
    Detect if the text is Bangla (Bijoy/Unicode) or English
    
    Args:
        text_sample: A sample of text to analyze
        
    Returns:
        'bangla' or 'english'
    """
    # Check for Bangla Unicode characters (U+0980 to U+09FF)
    bangla_unicode_pattern = re.compile(r'[\u0980-\u09FF]')
    
    # Check for common Bijoy ASCII characters that are used for Bangla
    # Bijoy uses ASCII characters in unusual ways (like `, ~, etc.)
    bijoy_pattern = re.compile(r'[`~©Ö¨«]')
    
    # Count Bangla indicators
    bangla_unicode_count = len(bangla_unicode_pattern.findall(text_sample))
    bijoy_count = len(bijoy_pattern.findall(text_sample))
    
    # If we find significant Bangla content, classify as Bangla
    if bangla_unicode_count > 5 or bijoy_count > 10:
        return 'bangla'
    
    # Check for English characters
    english_pattern = re.compile(r'[a-zA-Z]')
    english_count = len(english_pattern.findall(text_sample))
    
    # If mostly English characters, classify as English
    if english_count > bangla_unicode_count + bijoy_count:
        return 'english'
    
    # Default to Bangla for mixed or uncertain cases
    return 'bangla'


def extract_text_from_pdf_pymupdf(pdf_path):
    """Extract text using PyMuPDF (good for Bangla/Bijoy)"""
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def extract_text_from_pdf_pypdf2(pdf_path):
    """Extract text using PyPDF2 (good for English)"""
    text = ""
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            text += page_text + '\n\n'
    return text


def process_no_ocr_pdf(pdf_path, output_path, output_format='txt'):
    """
    Process PDF without OCR with automatic language detection
    Supports both Bangla (with Bijoy conversion) and English
    
    Args:
        pdf_path: Path to the input PDF file
        output_path: Path to save the output file
        output_format: 'txt' or 'docx'
        
    Returns:
        Path to the output file
    """
    print("Extracting text from PDF...")
    
    # First, try to extract a sample using PyMuPDF to detect language
    sample_text = ""
    try:
        doc = fitz.open(pdf_path)
        # Get text from first few pages for language detection
        for i, page in enumerate(doc):
            if i < 3:  # Check first 3 pages
                sample_text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"Error extracting sample: {e}")
        sample_text = ""
    
    # Detect the language
    detected_language = detect_language(sample_text)
    print(f"Detected language: {detected_language}")
    
    # Extract full text based on detected language
    if detected_language == 'bangla':
        # Use PyMuPDF for Bangla (better for Bijoy fonts)
        extracted_text = extract_text_from_pdf_pymupdf(pdf_path)
        # Convert Bijoy to Unicode if needed
        try:
            converted_text = unicodeconverter.convert_bijoy_to_unicode(extracted_text)
            final_text = converted_text
        except Exception as e:
            print(f"Bijoy conversion not needed or failed: {e}")
            final_text = extracted_text
    else:
        # Use PyPDF2 for English (better formatting)
        final_text = extract_text_from_pdf_pypdf2(pdf_path)
    
    # Save output based on format
    if output_format == 'txt':
        with open(output_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(final_text)
        print(f"✅ Text file saved to: {output_path}")
    
    elif output_format == 'docx':
        document = Document()
        for line in final_text.splitlines():
            if line.strip():  # Only add non-empty lines
                document.add_paragraph(line)
        document.save(output_path)
        print(f"✅ Word document saved to: {output_path}")
    
    return output_path


# Compatibility aliases for existing code
def convert_bijoy_pdf_to_unicode_txt(pdf_path, output_txt_path=None):
    """Legacy function - redirects to unified processor"""
    if output_txt_path is None:
        base_name = os.path.splitext(pdf_path)[0]
        output_txt_path = f"{base_name}.txt"
    return process_no_ocr_pdf(pdf_path, output_txt_path, 'txt')


def convert_bijoy_pdf_to_unicode_docx(pdf_path, output_docx_path=None):
    """Legacy function - redirects to unified processor"""
    if output_docx_path is None:
        base_name = os.path.splitext(pdf_path)[0]
        output_docx_path = f"{base_name}.docx"
    return process_no_ocr_pdf(pdf_path, output_docx_path, 'docx')


def pdf_to_text(pdf_path, txt_path):
    """Legacy function - redirects to unified processor"""
    return process_no_ocr_pdf(pdf_path, txt_path, 'txt')


# Main execution for testing
if __name__ == "__main__":
    # Test with your PDF files
    test_pdf = "test.pdf"
    output_txt = "output.txt"
    
    if os.path.exists(test_pdf):
        process_no_ocr_pdf(test_pdf, output_txt, 'txt')
    else:
        print("Please provide a test PDF file")
