from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

client = MongoClient('mongodb+srv://test:sparta@cluster0.v7au3.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta_plus_week4

import jwt
import datetime
import hashlib
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

SECRET_KEY = 'SPARTA'


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    if (token_receive == None):
        return render_template('index.html')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('index.html', user_info=user_info)
    except jwt.exceptions.DecodeError:
        return render_template('index.html')

# 유저가 입력한 제품 데이터를 db에 저장
@app.route("/item", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    category_receive = request.form['category_give']

    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"username": payload["id"]})


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    title = soup.select_one('div.style_inner__1Eo2z > div.top_summary_title__15yAr > h2').text
    image = soup.select_one('div.style_content__36DCX > div > div.image_thumb_area__1dzNx > div > div > img')["src"]
    price = soup.select_one('div.style_content__36DCX > div > div.summary_info_area__3XT5U > div.lowestPrice_price_area__OkxBK > div.lowestPrice_low_price__fByaG > em').text
    doc={
        "user":user_info['username'],
        "title":title,
        "image":image,
        "price":price,
        "star":star_receive,
        "comment":comment_receive,
        "category":category_receive
    }

    item_id = db.devItems.insert_one(doc).inserted_id

    return jsonify({'msg':'저장 완료!'})




# 각 카테고리 클릭시 get요청, url에 카테고리 이름을 붙여서 keyword로 전달, 그 변수를 이용해 db에서 해당 카테고리를 찾습니다.
# url이 다르므로 모든 데이터를 항상 변수 items로 전달해도 변수가 겹칠 일이 없다고 생각했습니다.
@app.route("/<keyword>", methods=["GET"])
def item_get(keyword):
    all_item = list(db.devItems.find({"category":keyword}, {'_id': False}))
    categoryName = keyword
    token_receive = request.cookies.get('mytoken')
    if (token_receive == None):
        return render_template('index.html',items=all_item)
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"username": payload["id"]})
    return render_template("index.html",items=all_item, user_info=user_info)

#로그인/회원가입 페이지
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

# 로그인
@app.route('/sign_in', methods=['POST'])
def sign_in():

    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    # 로그인이 성공하면
    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # 서버는 jwt토큰을 만들어서 클라이언트한테 발행 -> 클라이언트는 jwt토큰을 cookie에 저장했다가 유효할때까지 씀
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# 회원가입
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

#아이디 중복 체크
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)