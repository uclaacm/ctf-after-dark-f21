from bs4 import BeautifulSoup
from flask import Flask, flash, make_response, render_template, request, redirect, abort
from os import environ
from redis_namespace import StrictRedis
from uuid import uuid4
import re

app = Flask(__name__)
level = int(environ['XSS_LEVEL'])
redis = StrictRedis(
	host=environ.get('REDIS_HOST', 'localhost'),
	port=environ.get('REDIS_PORT', '6379'),
	namespace=f'{level}:')

keywords = ["fetch", "get", "post", "head", "put", "delete", "connect", 
        "options", "trace", "patch", "cookie", "document", "xmlhttprequest", "jquery",
        "ajax", "qwest", "superagent", "http", "client", "axios", "request", "xhr"]

triggers = ["script", "onabort", "onblur", "onchange", "onclick", "ondblclick",
        "ondragdrop", "onerror", "onfocus", "onkeydown", "onkeypress",
        "onkeyup", "onload", "onmousedown", "onmousemove", "onmouseout",
        "onmouseover", "onmouseup", "onmove", "onreset", "onresize", "onselect",
        "onsubmit", "onunload", "javascript"]

def filter(data):
        if (level == 1):
            data = data
        elif(level == 2):
            for word in keywords:
                if(re.search(word, data, flags=re.IGNORECASE)):
                    data = ""
                    break
        elif (level == 3):
            data = data
        elif (level == 4):
            for trig in triggers:
                if(re.search(trig, data, flags=re.IGNORECASE)):
                    data=""
                    break
        else:
            data=""
        return data

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/posts', methods=['POST'])
def submit():
	data = request.form['input']
	uuid = str(uuid4())
	redis.set(uuid, filter(data).encode())
	return redirect(f'/post/{uuid}')

@app.route('/view', methods=['POST'])
def view():
    return render_template('source.html', level = level)

@app.route('/post/<uuid>')
def level1(uuid):
	if redis.exists(uuid):
		resp = make_response(render_template('post.html', post=redis.get(uuid).decode()))
                if level == 3:
                    resp.headers['Content-Security-Policy'] = 'script-src notepad1.acmcyber.com'
		return resp
	abort(404)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
