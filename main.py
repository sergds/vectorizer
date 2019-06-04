import os
import time
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import platform

rp = os.path.realpath(__file__)
dirn = os.path.dirname(rp)
app = Flask(__name__)

def ensure_dir(dir):
    #directory = os.path.dirname(file_path)
    if not os.path.exists(dir):
        os.makedirs(dir)

print('Running on %s' % platform.system())
print('Lc: Cleaning up uploads...')
os.system('rm -rf %s/uploads/*' % dirn)
print('Lc: Done.')
print('Lc: Initializing app...')


PRIM_EXEC_PATH = '%s/bin' % dirn
UPLOAD_FOLDER = '%s/uploads' % dirn
ensure_dir(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
            #return send_from_directory(directory=uploads, filename=filename)
            if platform.system() == 'Darwin' :
                PLATFRM = 'primitive_darwin_amd64'
            if platform.system() == 'Linux' :
                PLATFRM = 'primitive_linux_amd64'
            if platform.system() == 'Windows' :
                PLATFRM = 'primitive_windows_amd64.exe'
            if platform.machine() == 'arm' :
                PLATFRM = 'primitive_linux_arm'
            if platform.machine() == 'armv7l' :
                PLATFRM = 'primitive_linux_arm'
            if platform.machine() == 'aarch64' :
                PLATFRM = 'primitive_linux_arm64'
            clim = '%s/%s -m 0 -v -n 115 -o uploads/tmp.png -i uploads/%s' % (PRIM_EXEC_PATH, PLATFRM, filename)
            #print(clim)
            os.system(clim)
            return redirect("/u/tmp.png")
    return '''
    <!doctype html>
    <title>Vectorizer 3000</title>
    <h1>Vectorize new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route("/u/<path:filename>", methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)
print('Lc: Running app...')
app.run(host='0.0.0.0')
