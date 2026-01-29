from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
import os
import sys
from werkzeug.utils import secure_filename

# Add the current directory to the Python path to ensure all modules are found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import functions from unified processing modules
from No_OCR_unified import process_no_ocr_pdf
from OCR_unified import process_ocr_pdf
from GenAI_unified import process_genai_pdf

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
        
        # For GenAI method, get the API key
        api_key = None
        if processing_method == 'genai':
            api_key = request.form.get('api_key')
            if not api_key or api_key.strip() == '':
                flash('API key is required for GenAI processing', 'error')
                return redirect(url_for('index'))
        
        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Generate output filename
        output_filename = os.path.splitext(filename)[0] + f".{output_format}"
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Process the file based on the selected method
        try:
            if processing_method == 'no_ocr':
                # No OCR - Auto-detect language (Bangla/English)
                process_no_ocr_pdf(filepath, output_filepath, output_format)
            
            elif processing_method == 'ocr':
                # OCR-based - Auto-detect language (Bangla/English)
                process_ocr_pdf(filepath, output_filepath, output_format)
            
            elif processing_method == 'genai':
                # GenAI-based - Google Gemini AI with language detection
                process_genai_pdf(filepath, output_filepath, output_format, api_key)
            
            else:
                flash('Invalid processing method selected', 'error')
                return redirect(url_for('index'))
            
            # Clean up the uploaded file after processing
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(f"Warning: Could not remove uploaded file: {e}")
            
            # Store the output filename in session for download
            return redirect(url_for('download_file', filename=output_filename))
            
        except Exception as e:
            # Error handling
            flash(f'Error processing PDF: {str(e)}', 'error')
            # Clean up uploaded file on error
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except:
                    pass
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

if __name__ == '__main__':
    app.run(debug=True)