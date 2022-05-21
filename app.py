from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import certifi
from yolov5 import detect

app = Flask(__name__)

#DB 연결 코드
from pymongo import MongoClient
client = MongoClient('')
db = client.dbsparta

# DB 연결 코드
from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://test:sparta@cluster0.ibmct.mongodb.net/?retryWrites=true&w=majority',
    tlsCAFile=certifi.where())

db = client.od_project

#최초 접속 시 연결되는 홈 페이지 지정
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload')
def upload():
    name_receive = request.form['name_give']
    file_receive = request.files['file_give']  # werkzeug.datastructures.FileStorage, name
    extension = secure_filename(file_receive.filename).split('.')[-1]  # file.filename /
    f_name = file_receive.filename.replace('.' + extension, '')  # test1, 확장자 제거

    # 파일 이름 , Local에 Upload 한 이미지 저장
    filename = f_name + '-'    # test1-2022-05-19-14-43-23.jpg
    upload_path = 'static/' + filename + '.' + extension
    file_receive.save(upload_path)  # 'static/test1.jpg

    classes = detect.run(upload_path)
    print(classes)

    # 아래와 같이 입력하면 db에 추가 가능!
    doc = {
        'name': name_receive,
        'file': upload_path,
        'classes': classes,
    }
    db.files.insert_one(doc)

    return jsonify({'result': 'success'})

@app.route('/search')
def upload():
    name_receive = request.form['name_give']

    db.files.find({'name': name_receive})


    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True) #기본포트값 5000으로 설정
