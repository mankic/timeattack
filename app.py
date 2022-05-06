from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta


app = Flask(__name__)
# app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

client = MongoClient('mongodb+srv://test:sparta@cluster0.fp2p3.mongodb.net/cluster0?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    return jsonify({'result': 'success'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    # 회원가입
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # DB에 저장
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
    }
    db.timeattack0506.insert_one(doc)

    return jsonify({'result': 'success'})

#
# @app.route('/sign_up/check_dup', methods=['POST'])
# def check_dup():
#     # ID 중복확인
#     return jsonify({'result': 'success'})
#

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)