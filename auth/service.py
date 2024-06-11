from flask import Flask, make_response, flash, send_from_directory,send_file,abort
from flask import render_template
from flask import url_for
from flask import request,redirect
from db_aux.db import register_user
from db_aux.db import get_user
import requests
import os
from datetime import datetime, timedelta
from queue_aux.queue import download_pdf_file
from werkzeug.utils import secure_filename
from aux.check_and_send_file import allowed_file, send_file_to_queue

app = Flask(__name__)
app.secret_key=os.environ.get('secret')

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
                    if 'doc' not in request.files:
                        return make_response(
                            render_template('service.html',error='Error: Any file uploaded')
                        )
                    file = request.files['doc']
                    if file.filename == '':
                        return make_response(
                            render_template('service.html',error='Error: No file selected')
                        )
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join('/app/files',filename))
                        message = send_file_to_queue(filename)
                        flash(message)
                        return redirect(url_for('download_pdf'))
                    else:
                        return make_response(
                            render_template('service.html',error='Error: Filetype not allowed')
                        )
                else:
                    return render_template('service.html')
            else:
                return redirect(url_for('init'))
        else:
            return redirect(url_for('init'))
        
@app.route("/download")
def download_pdf():
    if request.cookies.get('token_jwt'):
        r = requests.post(f"http://{os.environ.get('JWT_SERVICE')}/verify_jwt",
                        data={
                            "token":request.cookies.get('token_jwt'),
                        })
        if r.text == "True":
            return render_template('download.html')
        else:
            return redirect(url_for('init'))
    else:
        return redirect(url_for('init'))
    
@app.route("/file/<filename>")
def archive(filename):
    try:
        file = '/app/files/'+filename
        return send_file(file,as_attachment=True,download_name='your_pdf_file.pdf')
    except Exception as err:
        print(err)
        return abort(404)

