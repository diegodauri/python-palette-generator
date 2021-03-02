import os
from haishoku.haishoku import Haishoku
from flask import Flask, request, redirect, flash, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "./static/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config["SECRET_KEY"] = "KeyboardCat"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_palette(image):
    palette = Haishoku.getPalette(f"static/uploads/{image}")
    return palette


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
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
            return redirect(url_for("palette", filename=filename))
    return render_template("upload.html")


@app.route("/palette/<filename>")
def palette(filename):
    palette = get_palette(filename)
    return render_template("palette.html", image_url=f'{request.url.replace("palette", "static/uploads")}', palette=palette)


if __name__ == "__main__":
    app.run(debug=True)
