import pytesseract
import matplotlib.pyplot as plt
from PIL import Image
import os
from pdf2image import convert_from_path
import tempfile
import re

# For Windows users: Uncomment and update these paths if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
POPPLER_PATH = r'C:\Program Files\poppler-24.08.0\Library\bin'

def detect_language(text_sample):
    """
    Detect if text is primarily Bengali or English
    
    Args:
        text_sample: Sample text to analyze
        
    Returns:
        'ben' for Bengali, 'eng' for English
    """
    # Bengali Unicode range: \u0980-\u09FF
    bengali_pattern = re.compile(r'[\u0980-\u09FF]')
    bengali_chars = len(bengali_pattern.findall(text_sample))
    
    # If more than 10% of characters are Bengali, treat as Bengali
    if bengali_chars > len(text_sample) * 0.1:
        return 'ben'
    else:
        return 'eng'

def extract_text_from_pdf(pdf_path, output_txt_path=None, language=None):
    """
    Extract text from a PDF file using Tesseract
    
    Args:
        pdf_path: Path to the PDF file
        output_txt_path: Path to save the extracted text
        language: Specify 'ben' for Bengali, 'eng' for English, or None for auto-detection
        
    Returns:
        Extracted text
    """
    print("Converting PDF to images...")
    
    # Create a temporary directory for the image files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Convert PDF to images
        # For Windows users: add poppler_path=POPPLER_PATH to the arguments below if needed
        images = convert_from_path(pdf_path, dpi=300, output_folder=temp_dir, poppler_path=POPPLER_PATH)
        
        print(f"PDF has {len(images)} pages. Processing...")
        
        all_text = []
        detected_language = None
        
        # Process each page
        for i, image in enumerate(images):
            # Extract text with Tesseract
            print(f"Extracting text from page {i+1}...")
            
            # If language is not specified and this is the first page, attempt detection
            if language is None and detected_language is None:
                # First try with English for detection
                sample_text = pytesseract.image_to_string(image, config=r'--oem 3 --psm 6 -l eng')
                detected_language = detect_language(sample_text)
                print(f"Auto-detected language: {detected_language}")
            
            # Use the detected or specified language
            lang = language or detected_language
            custom_config = f'--oem 3 --psm 6 -l {lang}'
            
            extracted_text = pytesseract.image_to_string(image, config=custom_config)
            
            # Add page number for better organization
            page_text = f"--- Page {i+1} ---\n{extracted_text}\n\n"
            all_text.append(page_text)
        
        # Combine text from all pages
        full_text = "".join(all_text)
        
        # Save output if path is provided
        if output_txt_path:
            with open(output_txt_path, 'w', encoding='utf-8') as f:
                f.write(full_text)
            print(f"Extracted text saved to {output_txt_path}")
        
        return full_text

# Main execution
if __name__ == "__main__":
    # Update with your local paths
    pdf_path = "eng.pdf"  # PDF in the same directory as the script
    output_txt_path = "eng.txt"
    
    # You can specify language explicitly: 'ben' for Bengali, 'eng' for English
    # Or set to None for auto-detection
    language = None  # Auto-detect
    
    extracted_text = extract_text_from_pdf(pdf_path, output_txt_path, language)
    
    print("\n===== EXTRACTED TEXT PREVIEW =====")
    print(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
    print("==================================")


# Works for Bangla&English language. Slow Processing…
# Good for the CQ pdf files.
# Annoying header and footer texts.
