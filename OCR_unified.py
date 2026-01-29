import pytesseract
from PIL import Image
import os
from pdf2image import convert_from_path
import tempfile
import re

# For Windows users: Update these paths if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
POPPLER_PATH = r'C:\Program Files\poppler-24.08.0\Library\bin'


def detect_language_from_image(image):
    """
    Detect language from an image sample
    
    Args:
        image: PIL Image object
        
    Returns:
        'bangla', 'english', or 'mixed'
    """
    try:
        # Try detecting with Tesseract OSD (Orientation and Script Detection)
        osd = pytesseract.image_to_osd(image)
        
        # Check if Bengali script is detected
        if 'Bengali' in osd or 'Script: Bengali' in osd:
            return 'bangla'
        elif 'Latin' in osd or 'Script: Latin' in osd:
            return 'english'
    except:
        pass
    
    # Fallback: Try extracting with both languages and compare
    try:
        # Extract with English
        eng_text = pytesseract.image_to_string(image, lang='eng', config='--psm 6')
        # Extract with Bangla
        ben_text = pytesseract.image_to_string(image, lang='ben', config='--psm 6')
        
        # Count Bangla Unicode characters
        bangla_pattern = re.compile(r'[\u0980-\u09FF]')
        bangla_count = len(bangla_pattern.findall(ben_text))
        
        # Count English characters
        english_pattern = re.compile(r'[a-zA-Z]')
        english_count = len(english_pattern.findall(eng_text))
        
        if bangla_count > english_count:
            return 'bangla'
        elif english_count > bangla_count:
            return 'english'
        else:
            return 'mixed'
    except:
        # Default to mixed for safety
        return 'mixed'


def process_ocr_pdf(pdf_path, output_path, output_format='txt'):
    """
    Process PDF with OCR with automatic language detection
    Supports Bangla, English, and mixed language content
    
    Args:
        pdf_path: Path to the input PDF file
        output_path: Path to save the output file
        output_format: 'txt' or 'docx'
        
    Returns:
        Path to the output file
    """
    print("Converting PDF to images...")
    
    # Create a temporary directory for the image files
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path, dpi=300, output_folder=temp_dir, poppler_path=POPPLER_PATH)
            print(f"PDF has {len(images)} pages. Processing...")
        except Exception as e:
            print(f"Error converting PDF to images: {e}")
            raise
        
        # Detect language from first page
        if len(images) > 0:
            detected_language = detect_language_from_image(images[0])
            print(f"Detected language: {detected_language}")
        else:
            detected_language = 'mixed'
            print("No images found, defaulting to mixed language")
        
        # Set Tesseract language based on detection
        if detected_language == 'bangla':
            lang_config = 'ben+eng'  # Bangla primary, English secondary
            print("Using Bangla + English OCR")
        elif detected_language == 'english':
            lang_config = 'eng+ben'  # English primary, Bangla secondary
            print("Using English + Bangla OCR")
        else:
            lang_config = 'ben+eng'  # Mixed: try both
            print("Using mixed language OCR (Bangla + English)")
        
        all_text = []
        
        # Process each page
        for i, image in enumerate(images):
            print(f"Extracting text from page {i+1}...")
            
            try:
                # Use adaptive OCR configuration
                custom_config = f'--oem 3 --psm 6 -l {lang_config}'
                extracted_text = pytesseract.image_to_string(image, config=custom_config)
                
                # Add page number for better organization
                page_text = f"--- Page {i+1} ---\n{extracted_text}\n\n"
                all_text.append(page_text)
            except Exception as e:
                print(f"Error extracting text from page {i+1}: {e}")
                all_text.append(f"--- Page {i+1} ---\nError extracting text\n\n")
        
        # Combine text from all pages
        full_text = "".join(all_text)
        
        # Save output based on format
        if output_format == 'txt':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_text)
            print(f"✅ Extracted text saved to {output_path}")
        
        elif output_format == 'docx':
            from docx import Document
            document = Document()
            
            for line in full_text.splitlines():
                if line.strip():  # Only add non-empty lines
                    document.add_paragraph(line)
            
            document.save(output_path)
            print(f"✅ Word document saved to {output_path}")
        
        return output_path


# Compatibility aliases for existing code
def extract_bangla_text_from_pdf(pdf_path, output_txt_path=None):
    """Legacy function - redirects to unified processor"""
    if output_txt_path is None:
        base_name = os.path.splitext(pdf_path)[0]
        output_txt_path = f"{base_name}.txt"
    return process_ocr_pdf(pdf_path, output_txt_path, 'txt')


def extract_text_from_pdf(pdf_path, output_txt_path=None, language=None):
    """Legacy function - redirects to unified processor"""
    if output_txt_path is None:
        base_name = os.path.splitext(pdf_path)[0]
        output_txt_path = f"{base_name}.txt"
    # Ignore the language parameter as we now auto-detect
    return process_ocr_pdf(pdf_path, output_txt_path, 'txt')


# Main execution for testing
if __name__ == "__main__":
    # Test with your PDF files
    test_pdf = "test.pdf"
    output_txt = "output_ocr.txt"
    
    if os.path.exists(test_pdf):
        process_ocr_pdf(test_pdf, output_txt, 'txt')
    else:
        print("Please provide a test PDF file")
