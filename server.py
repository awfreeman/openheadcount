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
def generate():
	# grab global references to the output frame and lock variables
	global imglock
	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with imglock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if hct.outputframe is None:
				continue
			# encode the frame in JPEG format
			(flag, encodedImage) = cv.imencode(".jpg", hct.outputframe)
			# ensure the frame was successfully encoded
			if not flag:
				continue
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')
@app.route('/previewframe')
def getpreview():
	global imglock
	with imglock:
		(flag, encodedImage) = cv.imencode('.jpg', hct.outputframe)
		if not flag:
			return "No image"
		return Response(bytearray(encodedImage), mimetype = "image/jpeg; boundary=frame")

@app.route('/camerafeed')
def camerafeed():
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")
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
		coords = request.form['gridcoords']
		return coords
if __name__ == '__main__':
    app.run()