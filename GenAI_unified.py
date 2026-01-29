import os
import tempfile
from pdf2image import convert_from_path
from PIL import Image
import google.generativeai as genai
import io
import shutil
from docx import Document

# For Windows users: Update poppler path if needed
POPPLER_PATH = r'C:\Program Files\poppler-24.08.0\Library\bin'


def setup_gemini(api_key):
    """
    Set up Gemini model with provided API key
    
    Args:
        api_key: Google Gemini API key
        
    Returns:
        Initialized Gemini model or None if failed
    """
    genai.configure(api_key=api_key)
    model_name = 'gemini-2.0-flash-exp'
    
    print(f"Initializing Gemini model: {model_name}")
    try:
        model = genai.GenerativeModel(model_name)
        print("Model initialized successfully.")
        return model
    except Exception as e:
        print(f"Error initializing model '{model_name}': {e}")
        return None


def convert_pdf_to_images_genai(pdf_path):
    """
    Convert PDF to images for GenAI processing
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Tuple of (image_paths, temp_dir)
    """
    print("Converting PDF to images for GenAI processing...")
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return [], None

    temp_dir = tempfile.mkdtemp()
    print(f"Created temporary directory for images: {temp_dir}")

    try:
        images = convert_from_path(
            pdf_path,
            dpi=300,
            output_folder=temp_dir,
            fmt='jpeg',
            thread_count=4,
            paths_only=True,
            poppler_path=POPPLER_PATH
        )
        image_paths = images
        print(f"Converted {len(image_paths)} pages to images.")
        return image_paths, temp_dir
    except Exception as e:
        print(f"An error occurred during PDF to image conversion: {e}")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return [], None


def extract_text_from_image_genai(image_path, model):
    """
    Extract text from image using Gemini AI
    
    Args:
        image_path: Path to the image file
        model: Initialized Gemini model
        
    Returns:
        Extracted text or error message
    """
    if not model:
        print("Model not initialized, cannot extract text.")
        return None

    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return None

    try:
        img = Image.open(image_path)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        prompt = """
        Please perform OCR on this image.
        Extract all the text visible (Bangla, English, or mixed).
        Preserve the original structure, line breaks, and paragraph formatting as accurately as possible based on the visual layout.
        Do not add any commentary, explanations, or text other than the extracted content from the image.
        Output *only* the extracted text.
        """

        image_part = {"mime_type": "image/jpeg", "data": img_byte_arr}
        prompt_part = prompt

        response = model.generate_content([prompt_part, image_part])

        extracted_text = ""
        if hasattr(response, 'text'):
            extracted_text = response.text
        elif response.parts:
            extracted_text = "".join(part.text for part in response.parts if hasattr(part, 'text'))
        else:
            print(f"Warning: Could not extract text from response for {os.path.basename(image_path)}.")
            extracted_text = f"--- ERROR: Could not parse response for page {os.path.basename(image_path)} ---"

        return extracted_text

    except Exception as e:
        print(f"An error occurred during text extraction for {os.path.basename(image_path)}: {e}")
        return f"--- ERROR: Exception during extraction for page {os.path.basename(image_path)}: {e} ---"


def process_genai_pdf(pdf_path, output_path, output_format='txt', api_key=None):
    """
    Process PDF using GenAI (Google Gemini) with automatic language detection
    Supports Bangla, English, and mixed language content
    
    Args:
        pdf_path: Path to the input PDF file
        output_path: Path to save the output file
        output_format: 'txt' or 'docx'
        api_key: Google Gemini API key
        
    Returns:
        Path to the output file or raises exception on error
    """
    if not api_key:
        raise ValueError("API key is required for GenAI processing")
    
    # Initialize the Gemini model
    model = setup_gemini(api_key)
    if not model:
        raise Exception("Failed to initialize the Gemini model. Please check your API key.")
    
    # Convert PDF to images
    image_paths, temp_dir = convert_pdf_to_images_genai(pdf_path)
    if not image_paths or temp_dir is None:
        raise Exception("Failed to convert PDF to images.")
    
    # Extract text from images
    all_extracted_text = []
    has_errors = False
    
    for i, image_path in enumerate(image_paths):
        print(f"Processing page {i+1}/{len(image_paths)} with GenAI...")
        
        if not image_path or not os.path.exists(image_path):
            all_extracted_text.append(f"--- ERROR: Image file missing for page {i+1} ---")
            has_errors = True
            continue
        
        extracted_text = extract_text_from_image_genai(image_path, model)
        
        if extracted_text is None or "--- ERROR:" in extracted_text:
            all_extracted_text.append(extracted_text or f"--- ERROR EXTRACTING PAGE {i+1} ---")
            has_errors = True
        else:
            all_extracted_text.append(extracted_text)
    
    # Clean up temporary directory
    if temp_dir and os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Warning: Could not remove temporary directory {temp_dir}: {e}")
    
    # Save output based on format
    if output_format == 'txt':
        with open(output_path, 'w', encoding='utf-8') as txt_file:
            for i, page_text in enumerate(all_extracted_text):
                txt_file.write(f"--- Page {i+1} ---\n")
                txt_file.write(page_text)
                if i < len(all_extracted_text) - 1:
                    txt_file.write("\n\n--- Page Break ---\n\n")
        print(f"✅ GenAI extracted text saved to {output_path}")
    
    elif output_format == 'docx':
        document = Document()
        for page_text in all_extracted_text:
            document.add_paragraph(page_text)
            document.add_page_break()
        document.save(output_path)
        print(f"✅ GenAI Word document saved to {output_path}")
    
    if has_errors:
        print("⚠️ Some pages could not be processed correctly. Please check the output file.")
    
    return output_path
