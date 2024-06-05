import jwt
from flask import Flask
from flask import request
import os

key = os.environ.get('secret')

app = Flask(__name__)


@app.route("/generate_jwt", methods=["POST"])
def generate_jwt():
    try:
        id = request.form["id"]
        user = request.form["user"]
        payload={
            "id":id,
            "user":user
        }
        encoded = jwt.encode(payload,key,algorithm="HS256")
        return encoded
    except Exception as err:
        print("#"*159)
        print("oi")
        print(err)

@app.route("/generate_jwt", methods=["POST"])
def verify_jwt():
    token = request.form['token']
    decode = jwt.decode(token,key,algorithm="HS256")
    return decode

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80,debug=True)