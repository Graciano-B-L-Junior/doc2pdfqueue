from flask import Flask
from flask import render_template
from flask import url_for
from flask import request,redirect
from db_aux.db import register_user
from db_aux.db import get_user
import requests
import os

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def init():
    if request.method == 'GET':
        return render_template('index.html',)
    elif request.method == 'POST':
        login = request.form['login']
        passwd = request.form['senha']

        uid, name = get_user(login,passwd)
        if uid == None or name == None:
            return render_template('index.html',err='Usuário não existe')
        else:
            r = requests.post(f"http://{os.environ.get('JWT_SERVICE')}/generate_jwt",
                          data={
                              "id":uid,
                              "user":name
                          })
            print(r.text)
            return render_template('index.html',err='Deu certo a parada')
    else:
        return render_template('index.html',)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['senha']
        password2 = request.form['senha_2']
        if password != password2:
            return render_template('register.html', error='passwords needed to be iquals')
        else:
            if register_user(login,password):
                return redirect(url_for('init'))
            else:
                return render_template('register.html', error='Error occurred when try to register, try again later')