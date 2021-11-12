import itertools
import os
from flask import Flask, send_from_directory

app = Flask(__name__)
root = os.path.dirname(__file__)

@app.route('/<path:path>')
def index(path):
    return send_from_directory(root, path)
