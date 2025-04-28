import fitz  # PyMuPDF
import unicodeconverter
import os
from docx import Document

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

def convert_bijoy_pdf_to_unicode_docx(pdf_path, output_docx_path=None):
    # Generate output filename with same name as input if not provided
    if output_docx_path is None:
        base_name = os.path.splitext(pdf_path)[0]
        output_docx_path = f"{base_name}.docx"
    
    # Step 1: Extract text from PDF
    bijoy_text = extract_text_from_pdf(pdf_path)
    
    # Step 2: Convert Bijoy ASCII to Unicode Bangla
    unicode_text = unicodeconverter.convert_bijoy_to_unicode(bijoy_text)
    
    # Step 3: Write to a DOCX file
    document = Document()
    
    for line in unicode_text.splitlines():
        document.add_paragraph(line)
    
    document.save(output_docx_path)
    
    print(f"✅ Unicode Bangla Word file saved to: {output_docx_path}")
    return output_docx_path

def convert_bijoy_pdf_to_unicode_txt(pdf_path, output_txt_path=None):
    # Generate output filename with same name as input if not provided
    if output_txt_path is None:
        base_name = os.path.splitext(pdf_path)[0]
        output_txt_path = f"{base_name}.txt"
    
    # Step 1: Extract text from PDF
    bijoy_text = extract_text_from_pdf(pdf_path)
    
    # Step 2: Convert Bijoy ASCII to Unicode Bangla
    unicode_text = unicodeconverter.convert_bijoy_to_unicode(bijoy_text)
    
    # Step 3: Write to a TXT file
    with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(unicode_text)
    
    print(f"✅ Unicode Bangla text file saved to: {output_txt_path}")
    return output_txt_path

# No OCR approach.
# Only works fine with bangla pdf. English not supported.
# Accuracy is good.
# Formatting is pretty good for MCQ Pdfs.
