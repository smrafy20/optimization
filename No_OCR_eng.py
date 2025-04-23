import PyPDF2

def pdf_to_text(pdf_path, txt_path):
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Open text file in write mode
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            # Extract text from each page and write to text file
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                txt_file.write(text + '\n\n')
    
    # Removed print statement that was showing in output
    return txt_path

# NO OCR Approach
# Only work with english text pdfs.
# Accuracy and alignment is average.
# No header or footer and watermarks.
