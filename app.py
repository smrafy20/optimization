from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify, after_this_request, session
import os
import sys
import tempfile
import time
from werkzeug.utils import secure_filename

# Add the current directory to the Python path to ensure all modules are found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import functions from each PDF processing module
from No_OCR_bn_raw import convert_bijoy_pdf_to_unicode_txt, convert_bijoy_pdf_to_unicode_docx
from No_OCR_eng import pdf_to_text
from OCR_bn_raw import extract_bangla_text_from_pdf
from OCR_multi import extract_text_from_pdf
from OCR_multi_split import extract_bangla_text_from_pdf as extract_bangla_text_split

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pdf_processor_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Clear any previous flash messages when returning to home page
    session.pop('_flashes', None)
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_pdf():
    # Check if a file was uploaded
    if 'pdf_file' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)
    
    file = request.files['pdf_file']
    
    # Check if user did not select a file
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Get the selected processing method
        processing_method = request.form.get('processing_method')
        output_format = request.form.get('output_format', 'txt')
        
        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Generate output filename
        output_filename = os.path.splitext(filename)[0] + f".{output_format}"
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Process the file based on the selected method
        try:
            if processing_method == 'no_ocr_bangla':
                if output_format == 'txt':
                    convert_bijoy_pdf_to_unicode_txt(filepath, output_filepath)
                elif output_format == 'docx':
                    convert_bijoy_pdf_to_unicode_docx(filepath, output_filepath)
            
            elif processing_method == 'no_ocr_english':
                if output_format == 'txt':
                    pdf_to_text(filepath, output_filepath)
                elif output_format == 'docx':
                    # For DOCX output, we need to convert the extracted text to a Word document
                    # First get the text using the existing function
                    temp_txt_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{os.path.splitext(filename)[0]}.txt")
                    pdf_to_text(filepath, temp_txt_path)
                    
                    # Then convert the text file to DOCX
                    from docx import Document
                    document = Document()
                    
                    # Read the text file and add its content to the DOCX
                    with open(temp_txt_path, 'r', encoding='utf-8') as txt_file:
                        for line in txt_file:
                            document.add_paragraph(line.strip())
                    
                    # Save the DOCX file
                    document.save(output_filepath)
                    
                    # Remove the temporary text file
                    if os.path.exists(temp_txt_path):
                        os.remove(temp_txt_path)
            
            elif processing_method == 'ocr_bangla':
                if output_format == 'txt':
                    extract_bangla_text_from_pdf(filepath, output_filepath)
                elif output_format == 'docx':
                    # Similar approach: get text first, then convert to DOCX
                    temp_txt_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{os.path.splitext(filename)[0]}.txt")
                    extract_bangla_text_from_pdf(filepath, temp_txt_path)
                    
                    # Convert to DOCX
                    from docx import Document
                    document = Document()
                    
                    with open(temp_txt_path, 'r', encoding='utf-8') as txt_file:
                        for line in txt_file:
                            document.add_paragraph(line.strip())
                    
                    document.save(output_filepath)
                    
                    # Remove the temporary text file
                    if os.path.exists(temp_txt_path):
                        os.remove(temp_txt_path)
            
            elif processing_method == 'ocr_multi':
                language = request.form.get('language', None)  # Get language from form
                
                if output_format == 'txt':
                    extract_text_from_pdf(filepath, output_filepath, language)
                elif output_format == 'docx':
                    # Get text first, then convert to DOCX
                    temp_txt_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{os.path.splitext(filename)[0]}.txt")
                    extract_text_from_pdf(filepath, temp_txt_path, language)
                    
                    # Convert to DOCX
                    from docx import Document
                    document = Document()
                    
                    with open(temp_txt_path, 'r', encoding='utf-8') as txt_file:
                        for line in txt_file:
                            document.add_paragraph(line.strip())
                    
                    document.save(output_filepath)
                    
                    # Remove the temporary text file
                    if os.path.exists(temp_txt_path):
                        os.remove(temp_txt_path)
            
            elif processing_method == 'ocr_split':
                if output_format == 'txt':
                    extract_bangla_text_split(filepath, output_filepath, split_pages=True)
                elif output_format == 'docx':
                    # Get text first, then convert to DOCX
                    temp_txt_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{os.path.splitext(filename)[0]}.txt")
                    extract_bangla_text_split(filepath, temp_txt_path, split_pages=True)
                    
                    # Convert to DOCX
                    from docx import Document
                    document = Document()
                    
                    with open(temp_txt_path, 'r', encoding='utf-8') as txt_file:
                        for line in txt_file:
                            document.add_paragraph(line.strip())
                    
                    document.save(output_filepath)
                    
                    # Remove the temporary text file
                    if os.path.exists(temp_txt_path):
                        os.remove(temp_txt_path)
            
            else:
                flash('Invalid processing method selected', 'error')
                return redirect(url_for('index'))
            
            # No more flash success message here - we'll show success on the download complete page
            
            # Store the output filename in session for download
            return redirect(url_for('download_file', filename=output_filename))
            
        except Exception as e:
            # Error handling
            flash(f'Error processing PDF: {str(e)}', 'error')
            return redirect(url_for('index'))
    else:
        flash('Invalid file format. Only PDF files are allowed.', 'error')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    # Set the file path
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Add a completion template that will auto-redirect with JavaScript
    if request.args.get('direct') == 'true':
        # Direct download without the intermediate page
        return send_file(file_path, as_attachment=True)
    else:
        # Show a download completion page that includes JavaScript to redirect
        return render_template('download_complete.html', filename=filename)

@app.route('/direct-download/<filename>')
def direct_download(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

@app.route('/check-status', methods=['GET'])
def check_status():
    """API endpoint to check the status of a file processing job"""
    # This is a placeholder for real-time status updates
    # In a production app, you would track job status in a database or queue system
    return jsonify({
        'status': 'processing',
        'progress': 75,
        'message': 'Processing your PDF...'
    })

if __name__ == '__main__':
    app.run(debug=True)