import os
import time
from flask import Flask, flash, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
import platform
from PIL import Image
import atexit
import random
import shutil
#import zipfile
#from zipfile import ZipFile
@atexit.register
def cleanuploads():
    print("Lc: Cleaning up uploads...")
    shutil.rmtree("uploads")
rp = os.path.realpath(__file__)
dirn = os.path.dirname(rp)
app = Flask(__name__)

def ensure_dir(dir):
    #directory = os.path.dirname(file_path)
    if not os.path.exists(dir):
        os.makedirs(dir)

print('Running on %s' % platform.system())
if os.path.exists("uploads"):
    print('Lc: Cleaning up uploads...')
    os.system('rm -rf %s/uploads/*' % dirn)
print('Lc: Done.')
print('Lc: Initializing app...')

# SETTINGS
BIN_PATH = '%s/bin' % dirn
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
            #uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
            #return send_from_directory(directory=uploads, filename=filename)
            im = Image.open("uploads/" + filename)
            h, w = im.size
            im.close()
            if h > 1920 or w > 1080:
                return "Sorry, max resolution is 1920x1080"
                
            jn = random.randint(1, 10000000)
            ARMMODE = 0
            if platform.system() == 'Darwin' :
                PLATFRM = 'primitive_darwin_amd64'
            if platform.system() == 'Linux' :
                PLATFRM = 'primitive_linux_amd64'
            if platform.system() == 'Windows' :
                PLATFRM = 'primitive_windows_amd64.exe'
            if platform.machine() == 'arm' :
                ARMMODE = 1
                PLATFRM = 'primitive_linux_arm'
            if platform.machine() == 'armv7l' :
                ARMMODE = 1
                PLATFRM = 'primitive_linux_arm'
            if platform.machine() == 'aarch64' :
                ARMMODE = 1
                PLATFRM = 'primitive_linux_arm64'
            if ARMMODE == 1:
                #with ZipFile(ZBIN_PATH, 'r') as zbin:
                #    zbin.extract(PLATFRM, path='/tmp', pwd='test')
                #ZBIN_FILE = '/tmp/%s' % PLATFRM
                #os.chmod(ZBIN_FILE, 0o777)
                clim = '%s/%s -m 1 -v -n 100 -o uploads/%s.png -i uploads/%s' % (BIN_PATH, PLATFRM, jn, filename)
            else:
                #with ZipFile(ZBIN_PATH, 'r') as zbin:
                 #   zbin.extract(PLATFRM, path='/tmp', pwd='test')
                #ZBIN_FILE = '/tmp/%s' % PLATFRM
                #os.chmod(ZBIN_FILE, 0o777)
                clim = '%s/%s -m 0 -v -n 115 -o uploads/%s.png -i uploads/%s' % (BIN_PATH, PLATFRM, jn, filename)
            #print(clim)
            os.system(clim)
            #os.remove(ZBIN_FILE)
            return redirect("/u/%s.png" % jn)
    return '''
    <!doctype html>
    <title>Vectorizer 3000</title>
    <h1>Vectorize new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=vectorize>
    </form>
    <h3>It Uses primitive by Michael Fogleman</h3>
    <h3>Process is long, so you have to wait</h3>
    <h3>Max resolution is 1920x1080</h3>
    '''

@app.route("/u/<path:filename>", methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)
#print('Lc: Running app...')
#app.run(host='0.0.0.0', port=5000, debug=False)
