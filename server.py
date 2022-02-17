from flask import Flask, render_template, request, Response, make_response
from usermgmt import usermgmt
import threading
from headcounter import headcounter
import numpy as np
import cv2 as cv
import time
import random
import sys

CONFIDENCE = .4
THRESHOLD = 15
HISTORY = 3
PATH = "vid.mp4"
threshold = THRESHOLD
history = HISTORY
app = Flask(__name__)
sessiontokens = dict()
hct = headcounter()
stoplock = threading.Lock()
getlock = threading.Lock()
imglock = threading.Lock()
path = 'vid.mp4'
vertexes = np.array([(0, 372//2), (250, 372//3),
                    (499, 372//2), (499, 372), (0, 372)])
expirytime=60*30
t1 = threading.Thread(target=hct.run, args=(
    stoplock, getlock, imglock, path, vertexes, threshold, history))
t1.start()

def authorize(auth):
    try:
        if (time.time()-sessiontokens[auth])> expirytime:
            return False
    except KeyError:
        return False
    return True


@app.route('/CONFIGURI', methods=['POST'])
def configuri():
    global t1
    global path
    auth = request.cookies.get('auth')
    if not authorize(auth):
        return 'Unauthorized'
    path = request.json
    with stoplock:
        hct.stop = True
    while t1.is_alive():
        continue
    hct.stop = False
    t1 = threading.Thread(target=hct.run, args=(
        stoplock, getlock, imglock, path, vertexes, threshold, history))
    t1.start()
    return 'Changed successfully'


@app.route('/CONFIGTHRESH', methods=['POST'])
def configthresh():
    global t1
    global threshold
    auth = request.cookies.get('auth')
    if not authorize(auth):
        return 'Unauthorized'
    with stoplock:
        hct.stop = True
    while t1.is_alive():
        continue
    hct.stop = False
    try:
        threshold = float(request.json)
        ret = "Successfully Changed"
    except ValueError:
        ret = "invalid value"
    t1 = threading.Thread(target=hct.run, args=(
        stoplock, getlock, imglock, path, vertexes, threshold, history))
    t1.start()
    return ret


@app.route('/CONFIGHIST', methods=['POST'])
def confighist():
    global t1
    global history
    auth = request.cookies.get('auth')
    if not authorize(auth):
        return 'Unauthorized'
    with stoplock:
        hct.stop = True
    while t1.is_alive():
        continue
    hct.stop = False
    try:
        history = int(request.json)
        ret = "Successfully Changed"
    except ValueError:
        ret = "invalid value"
    t1 = threading.Thread(target=hct.run, args=(
        stoplock, getlock, imglock, path, vertexes, threshold, history))
    t1.start()
    return ret


@app.route('/previewframe')
def getpreview():
    global imglock
    global sessiontokens
    auth = request.cookies.get('auth')
    if not authorize(auth):
        return 'Unauthorized'
    with imglock:
        (flag, encodedImage) = cv.imencode('.jpg', hct.outputframe)
        if not flag:
            return "No image"
        return Response(bytearray(encodedImage), mimetype="image/jpeg; boundary=frame")


@app.route('/preview')
def login_user(uname):
    global sessiontokens
    res = make_response(render_template('preview.html'))
    token = str(random.SystemRandom().getrandbits(4096))
    sessiontokens.update({token: time.time()})
    res.set_cookie('auth', token, max_age=60*30)
    return res


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


@app.route('/configurezones', methods=['POST', 'GET'])
def configurezones():
    if request.method == 'GET':
        auth = request.cookies.get('auth')
        if not authorize(auth):
            return 'Unauthorized'
        return render_template('configzones.html')
    elif request.method == 'POST':
        global t1
        global vertexes
        # get the points given
        vertexes = np.array(request.get_json())
        if len(vertexes) < 3:
            return "Invalid point selection"
        with stoplock:
            hct.stop = True
        while t1.is_alive():
            continue
        hct.stop = False
        t1 = threading.Thread(target=hct.run, args=(
            stoplock, getlock, imglock, path, vertexes))
        t1.start()
        return "Recieved"


'''
@app.route('/SHUTDOWN', methods['POST'])
def shutdown():
	global stoplock
	global t1
	global history
	global threshold
	global vertexes
	global path

	with stoplock:
		hct.stop = True
	while t1.is_alive():
		continue
	if verify(request.json):
		exit()
'''
if __name__ == '__main__':
    app.run()
