import os
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pdf2docx import Converter
import tempfile
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'bangla-pdf-converter')

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
ALLOWED_EXTENSIONS = {'pdf'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit upload size to 16MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
            
        file = request.files['file']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            # Generate a unique filename
            filename = secure_filename(file.filename)
            unique_id = uuid.uuid4().hex
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
            file.save(file_path)
            
            # Convert PDF to DOCX
            try:
                output_filename = f"{unique_id}_{os.path.splitext(filename)[0]}.docx"
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                
                # Convert PDF to DOCX
                cv = Converter(file_path)
                cv.convert(output_path)
                cv.close()
                
                return send_file(output_path, as_attachment=True)
            except Exception as e:
                flash(f'Error converting file: {str(e)}')
                return redirect(request.url)
            finally:
                # Clean up files
                if os.path.exists(file_path):
                    os.remove(file_path)
                
        else:
            flash('Only PDF files are allowed')
            return redirect(request.url)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)