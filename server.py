from flask import Flask, render_template, request
from usermgmt import usermgmt

app = Flask(__name__)

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
if __name__ == '__main__':
    app.run()