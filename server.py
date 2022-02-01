from flask import Flask, render_template, request, Response
from usermgmt import usermgmt
import threading
from headcounter import headcounter
import numpy as np
import cv2 as cv

app = Flask(__name__)

hct = headcounter()
lock = threading.Lock()
getlock = threading.Lock()
imglock = threading.Lock()
path = 'vid.mp4'
vertexes = np.array([(0, 372//2), (250, 372//3), (499, 372//2), (499, 372), (0, 372)])
t1 = threading.Thread(target=hct.run, args=(lock, getlock, imglock, path, vertexes))
t1.start()

@app.route('/previewframe')
def getpreview():
	global imglock
	with imglock:
		(flag, encodedImage) = cv.imencode('.jpg', hct.outputframe)
		if not flag:
			return "No image"
		return Response(bytearray(encodedImage), mimetype = "image/jpeg; boundary=frame")

def login_user(uname):
    return render_template('preview.html')
@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if usermgmt.authenticate(request.form['username'], request.form['password']):
            return login_user(request.form['username'])
        else:
            error = 'Invalid login'
    return render_template('login.html', error=error)

@app.route('/configure', methods=['POST', 'GET'])
def configure():
	if request.method == 'GET':
		return render_template('config.html')
	elif request.method == 'POST':
		json = request.get_json()
		points = convert_to_numpy(json)

		return "Recieved"
if __name__ == '__main__':
    app.run()