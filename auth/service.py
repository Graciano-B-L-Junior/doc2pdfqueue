from flask import Flask
from flask import render_template
from flask import url_for
from flask import request,redirect
from db_aux.db import register_user

app = Flask(__name__)

@app.route("/")
def init():
    return render_template('index.html',)

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == 'GET':
        return render_template('register.html')
    if request.method == "POST":
        login = request.form['login']
        password = request.form['senha']
        password2 = request.form['senha_2']
        if password != password2:
            return render_template('register.html', error='passwords needed to be iquals')
        else:
            if register_user(login,password):
                return redirect(url_for('init'))
            else:
                render_template('register.html', error='Error occurred when try to register, try again later')