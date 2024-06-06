from flask import Flask, make_response
from flask import render_template
from flask import url_for
from flask import request,redirect
from db_aux.db import register_user
from db_aux.db import get_user
import requests
import os
from datetime import datetime, timedelta

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
            token = r.text
            
            if token == "failed":
                return render_template('index.html',err='Erro ao gerar token de acesso, tente mais tarde')
            

            response = redirect(url_for('service',))

            response.set_cookie('token_jwt',token,expires=datetime.now() + timedelta(hours=1))

            
            
            return response
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
            
@app.route("/service", methods=["GET","POST"])
def service():
        if request.cookies.get('token_jwt'):
            r = requests.post(f"http://{os.environ.get('JWT_SERVICE')}/verify_jwt",
                          data={
                              "token":request.cookies.get('token_jwt'),
                          })
            if r.text == "True":
                if request.method == 'GET':
                    return render_template('service.html')
                elif request.method == 'POST':
                    ...
                else:
                    return render_template('service.html')
            else:
                return redirect(url_for('init'))
        else:
            return redirect(url_for('init'))