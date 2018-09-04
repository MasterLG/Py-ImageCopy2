import os
from flask import Flask, flash, request, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'YOUR DIRECTORY' # don't forget to put double backslashes
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = 'random string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# checks if the UPLOAD_FOLDER exists, if not creates


def directory_create():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

# checks if the file extension in in the allowed set


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file added!')
            return render_template('index.html')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return render_template('index.html')
        # check if the file has an allowed extension
        if not allowed_file(file.filename):
            flash('File extension not allowed!')
            return render_template('index.html')
        else:
            filename = secure_filename(file.filename)
            # create directory if does not exist
            directory_create()
            # file save
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return filename+" uploaded!"
    # return if the method is GET
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
