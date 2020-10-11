from flask import render_template
from app import app

from app.previewMusic import haalAlbums

@app.route('/')
@app.route('/index/')
def index():
    regels = haalAlbums(None)
    return render_template('index.html', regels=regels)

@app.route('/NL/')
def NL():
    regels = haalAlbums('NL')
    return render_template('index.html', regels=regels)