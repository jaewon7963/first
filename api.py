from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <h1>이미지 업로드</h1>
    <p>사진을 골라주세요</p>
    <form method="POST" action="/UNITE" enctype="multipart/form-data" accept-charset="cp949">
        <input type="file" name="file">
        <input type="submit" value="업로드">
    </form>
    <br>
    <form method="POST" action="/TEXT" enctype="multipart/form-data" accept-charset="cp949">
        <input type="file" name="text_file">
        <input type="submit" value="텍스트 파일 업로드">
    </form>
    '''


@app.route('/UNITE', methods=['POST'])
def detect_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    file = request.files['file']
    
    # 파일 저장
    upload_path = 'C:/Users/jjw79/capstone/project/CRAFT-pytorch/test/'
    file.save(os.path.join(upload_path, file.filename))
    
    # CRAFT 실행
    craft_path = r'C:/Users/jjw79/capstone/project/CRAFT-pytorch'
    subprocess.run(['python', os.path.join(craft_path, 'test.py')])

    # Recognition 실행
    recognition_path = r'C:/Users/jjw79/capstone/project/deep-text-recognition-benchmark-master'
    subprocess.run(['python', os.path.join(recognition_path, 'demo.py')])

    # 결과 파일 읽기
    
    with open(os.path.join(recognition_path + '/result/', 'recog_result.txt'), 'r', encoding='cp949') as f:
        result = f.read()
    result_utf8 = result.encode().decode('unicode_escape')
    
    return jsonify({'result': result_utf8})
    
@app.route('/TEXT', methods=['POST'])
def upload_text():
    if 'text_file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    text_file = request.files['text_file']
    with open(text_file, 'r') as f:
        result = f.read()
    result_utf8 = result.encode().decode('unicode_escape')

    return jsonify({'result': result_utf8})

if __name__ == '__main__':
    app.run(port = 8080)