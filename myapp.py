import atexit
import os
import platform
import shutil
from random import randint

from PIL import Image
from flask import Flask, flash, request, redirect, send_from_directory, render_template
from werkzeug.utils import secure_filename


@atexit.register
def cleanuploads():
    if os.path.exists("uploads"):
        print("Lc: Cleaning up uploads...")
        shutil.rmtree("uploads")
rp = os.path.realpath(__file__)
dirn = os.path.dirname(rp)
app = Flask(__name__)
app.secret_key = "testok"
def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


print('Running on %s' % platform.system())

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
            flash('ERROR:No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('ERROR:No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            im = Image.open("uploads/" + filename)
            h, w = im.size
            im.close()
            if h > 1920 and w > 1080:
                flash("ERROR:Sorry, max resolution is 1920x1080")
                return redirect(request.url)
            jn = randint(1, 10000000)
            arm_mode = 0
            if platform.system() == 'Darwin':
                executable = 'primitive_darwin_amd64'
            if platform.system() == 'Linux':
                executable = 'primitive_linux_amd64'
            if platform.system() == 'Windows':
                executable = 'primitive_windows_amd64.exe'
            if platform.machine() == 'arm':
                arm_mode = 1
                executable = 'primitive_linux_arm'
            if platform.machine() == 'armv7l':
                arm_mode = 1
                executable = 'primitive_linux_arm'
            if platform.machine() == 'aarch64':
                arm_mode = 1
                executable = 'primitive_linux_arm64'
            if arm_mode == 1:
                clim = '%s/%s -m 1 -v -n 100 -o uploads/%s.png -i uploads/%s' % (BIN_PATH, executable, jn, filename)
            else:
                clim = '%s/%s -m 1 -v -n 145 -o uploads/%s.png -i uploads/%s' % (BIN_PATH, executable, jn, filename)
            os.system(clim + "&")
            return redirect("/job/%s/%s/%s" % (jn, h, w))
    return render_template('index.html')


@app.route("/job/<jobid>/<height>/<width>") #(jobid, height, width)
def retjob(jobid, height, width):
    return render_template('job.html', jobid=jobid, height=height, width=width)


@app.route("/u/<path:filename>", methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)


@app.route("/assets/<path:filename>", methods=['GET', 'POST'])
def assets(filename):
    return send_from_directory(directory="assets", filename=filename)
