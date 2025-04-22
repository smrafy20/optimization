import pytesseract
import matplotlib.pyplot as plt
from PIL import Image
import os
from pdf2image import convert_from_path
import tempfile

# For Windows users: Uncomment and update these paths if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
POPPLER_PATH = r'C:\Program Files\poppler-24.08.0\Library\bin'

def extract_bangla_text_from_pdf(pdf_path, output_txt_path=None):
    """
    Extract Bangla and English text from a PDF file using Tesseract
    
    Args:
        pdf_path: Path to the PDF file
        output_txt_path: Path to save the extracted text
        
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
        
        # Process each page
        for i, image in enumerate(images):
            # Display the image
            # plt.figure(figsize=(10, 10))
            # plt.imshow(image)
            # plt.axis('off')
            # plt.title(f"Page {i+1}")
            # plt.show()
            
            # Extract text with Tesseract - using both Bengali and English languages
            print(f"Extracting text from page {i+1}...")
            custom_config = r'--oem 3 --psm 6 -l ben+eng'  # Use both Bangla and English languages
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
    pdf_path = "ict.pdf"  # PDF in the same directory as the script
    output_txt_path = "ict.txt"
    
    extracted_text = extract_bangla_text_from_pdf(pdf_path, output_txt_path)
    
    print("\n===== EXTRACTED TEXT PREVIEW =====")
    print(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
    print("==================================")