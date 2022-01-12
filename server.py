from flask import Flask, render_template, request

app = Flask(__name__)
def login_user(uname):
    return 'login success'
def valid_login(uname, passwd):
    if uname == 'admin':
        return True
    return False
@app.route('/')
def homepage():
    return render_template('index.html')
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return login_user(request.form['username'])
        else:
            error = 'Invalid login'
    return render_template('login.html', error=error)
if __name__ == '__main__':
    app.run()