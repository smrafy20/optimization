import pytesseract
import matplotlib.pyplot as plt
from PIL import Image
import os
from pdf2image import convert_from_path
import tempfile
import numpy as np

# For Windows users: Uncomment and update these paths if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
POPPLER_PATH = r'C:\Program Files\poppler-24.08.0\Library\bin'

def extract_bangla_text_from_pdf(pdf_path, output_txt_path=None, split_pages=True):
    """
    Extract Bangla and English text from a PDF file using Tesseract
    
    Args:
        pdf_path: Path to the PDF file
        output_txt_path: Path to save the extracted text
        split_pages: Whether to split each physical page into left and right sides
        
    Returns:
        Extracted text
    """
    print("Converting PDF to images...")
    
    # Create a temporary directory for the image files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=300, output_folder=temp_dir, poppler_path=POPPLER_PATH)
        
        print(f"PDF has {len(images)} physical pages. Processing...")
        
        all_text = []
        page_count = 0
        
        # Process each page
        for i, image in enumerate(images):
            if split_pages:
                # Get the width and height of the image
                width, height = image.size
                mid_point = width // 2
                
                # Split the image into left and right halves
                left_half = image.crop((0, 0, mid_point, height))
                right_half = image.crop((mid_point, 0, width, height))
                
                # Process each half as a separate page
                for half_idx, half_image in enumerate([left_half, right_half]):
                    page_count += 1
                    
                    # Optional: Display the half image
                    # plt.figure(figsize=(8, 10))
                    # plt.imshow(half_image)
                    # plt.axis('off')
                    # plt.title(f"Page {page_count} (Physical page {i+1}, {'Left' if half_idx == 0 else 'Right'})")
                    # plt.show()
                    
                    # Extract text with Tesseract
                    print(f"Extracting text from page {page_count} (Physical page {i+1}, {'Left' if half_idx == 0 else 'Right'})...")
                    custom_config = r'--oem 3 --psm 6 -l ben+eng'
                    extracted_text = pytesseract.image_to_string(half_image, config=custom_config)
                    
                    # Add page number for better organization
                    page_text = f"--- Page {page_count} (Physical page {i+1}, {'Left' if half_idx == 0 else 'Right'}) ---\n{extracted_text}\n\n"
                    all_text.append(page_text)
            else:
                # Process the entire page as one logical page
                page_count += 1
                
                # Extract text with Tesseract - using both Bengali and English languages
                print(f"Extracting text from page {page_count}...")
                custom_config = r'--oem 3 --psm 6 -l ben+eng'  # Use both Bangla and English languages
                extracted_text = pytesseract.image_to_string(image, config=custom_config)
                
                # Add page number for better organization
                page_text = f"--- Page {page_count} ---\n{extracted_text}\n\n"
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
    pdf_path = "bmcq.pdf"  # PDF in the same directory as the script
    output_txt_path = "bmcq.txt"
    
    # Set split_pages=True to process each page as two separate pages (left and right)
    extracted_text = extract_bangla_text_from_pdf(pdf_path, output_txt_path, split_pages=True)
    
    print("\n===== EXTRACTED TEXT PREVIEW =====")
    print(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
    print("==================================")