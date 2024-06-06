import jwt
from flask import Flask
from flask import request
import os
from datetime import datetime, timedelta

key = os.environ.get('secret')

app = Flask(__name__)


@app.route("/generate_jwt", methods=["POST"])
def generate_jwt():
    try:
        id = request.form["id"]
        user = request.form["user"]
        payload={
            "id":id,
            "user":user,
            "exp": datetime.now() + timedelta(seconds=10)
        }
        encoded = jwt.encode(payload,key,algorithm="HS256")
        return encoded
    except Exception as err:
        print(err)
    
    return "failed"

@app.route("/verify_jwt", methods=["POST"])
def verify_jwt():
    try:
        token = request.form['token']
        decode = jwt.decode(token,key,algorithms=["HS256"])
        return "True"
    except Exception as err:
        print(err)
    return "False"

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80,debug=True)