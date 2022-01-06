from flask import Flask, flash, request, redirect, render_template
import visual_match
from PIL import Image
import base64
import io

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_validated_file(html_name):
    # check for error in post request
    if html_name not in request.files:
        flash(f'POST error: {html_name}')
        raise ValueError("POST failed")

    file = request.files[html_name]

    # check if user failed to submit a file
    if file.filename == '':
        flash(f'File not selected: {html_name}')
        raise ValueError("One or more files not submitted")

    # check if file is allowed
    if file and allowed_file(file.filename):
        return file
    else:
        raise ValueError("Error reading files")

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        try:
            piece_file, board_file = get_validated_file('piece-file'), get_validated_file('board-file')
        except ValueError:
            return redirect(request.url)
        
        solution_image = visual_match.match(piece_file, board_file)
        solution_image = Image.fromarray(solution_image)
        data_buffer = io.BytesIO()
        solution_image.save(data_buffer, "PNG")
        encoded_data = base64.b64encode(data_buffer.getvalue())

        return render_template('index.html', image=encoded_data.decode('utf-8'))
    
    return render_template('index.html')
