import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from flask_mail import Mail, Message
import hashlib
import time
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies, verify_jwt_in_request
from datetime import datetime
import datetime
import string
import random
from flask_wtf.csrf import CSRFProtect
app = Flask(__name__)
csrf = CSRFProtect()
app.secret_key = 'root'
current_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_directory, "database.db")
mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'dage8044@gmail.com'
app.config['MAIL_PASSWORD'] = 'avdqyusbplgscqrd'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SECRET_KEY'] = 'root'  # 시크릿 키 설정
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=5)  # 토큰 만료 시간 설정 (1시간)
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
jwt = JWTManager(app)
mail = Mail(app)
temporary_tokens = {}
app.config['WTF_CSRF_ENABLED'] = True
csrf.init_app(app)
def get_db():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 딕셔너리 형태로 데이터 사용 가능
    return conn

# index 라우트에서 로그인 처리
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = request.form['id']
        password = request.form['pw']

        connection = get_db()
        cursor = connection.cursor()
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        # 데이터베이스에서 사용자 정보를 검색
        cursor.execute('SELECT * FROM members WHERE id=? AND passwd=?', (user_id, password))
        user_data = cursor.fetchone()

        if user_data:
            # 로그인 성공 시 JWT 토큰 발급
            access_token = create_access_token(identity=user_id)

            # 토큰을 브라우저에 쿠키로 설정하여 전달
            response = redirect(url_for('success', username = user_id))
            response.set_cookie('access_token_cookie', access_token, httponly=True)
            

            connection.close()
            return response
        else:
            connection.close()
            return render_template('Main.html', error="아이디 또는 비밀번호가 잘못되었습니다.")
    else:
        access_token = request.cookies.get('access_token_cookie')
        if access_token:
            verify_jwt_in_request() 
            return redirect(url_for('success', username = get_jwt_identity()))
        return render_template('Main.html')


# 로그아웃 시 토큰 삭제
@app.route('/logout', methods = ['GET','POST'])
def logout():
    session.pop('username', None)
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('access_token_cookie')
    return response

@app.route('/register', methods=['GET', 'POST'])
def register_post():
    if request.method == 'POST':
        user_id = request.form['regi_id']
        password = request.form['regi_pw']
        user_name = request.form['regi_name']
        email = request.form['regi_email']

        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        connection = get_db()
        cursor = connection.cursor()

        # 아이디 중복 검사
        cursor.execute('SELECT COUNT(*) FROM members WHERE id = ?', (user_id,))
        if cursor.fetchone()[0] > 0:
            connection.close()
            return render_template('register.html', error="이미 존재하는 아이디입니다.")
        
        # 닉네임 중복 검사
        cursor.execute('SELECT COUNT(*) FROM members WHERE name = ?', (user_name,))
        if cursor.fetchone()[0] > 0:
            connection.close()
            return render_template('register.html', error="이미 존재하는 닉네임입니다.")

        # 이메일 중복 검사
        cursor.execute('SELECT COUNT(*) FROM members WHERE email = ?', (email,))
        if cursor.fetchone()[0] > 0:
            connection.close()
            return render_template('register.html', error="이미 존재하는 이메일입니다.")

        # 새로운 사용자 추가
        cursor.execute('INSERT INTO members (id, passwd, name, email) VALUES (?, ?, ?, ?)', (user_id, password, user_name, email))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))
    else:
         return render_template('register.html')


@app.route('/findpasswd', methods=['GET', 'POST'])
def findpasswd():
    if request.method == 'POST':
        user_id = request.form['regi_id']
        user_name = request.form['regi_name']
        email = request.form['regi_email']

        connection = get_db()
        cursor = connection.cursor()

        # 사용자 정보 검색
        cursor.execute('SELECT * FROM members WHERE id = ? AND name = ? AND email = ?', (user_id, user_name, email))
        user_data = cursor.fetchone()
        # 바꿔야 함... 비밀번호 변경페이지로 유도로해야겠당
        if user_data:
            expiration_time = time.time() + 3600
            token = generate_token()
            temporary_tokens[token] = expiration_time
            reset_url = f'http://127.0.0.1:5000/resetpasswd?token={token}'
            msg = Message('Hello', sender='dage8044@gmail.com', recipients=[user_data['email']])
            msg.body = f'비밀번호를 변경하려면 아래 링크를 클릭하세요 {reset_url}'
            mail.send(msg)
            flash("이메일로 전송이 완료되었습니다 이메일을 확인해주세요")
            cursor.close()
            return redirect(url_for('index'))
        else:
            flash("일치하는 사용자 정보를 찾을 수 없습니다.")
            return render_template('findpasswd.html')
    else:
        return render_template('findpasswd.html')
def generate_token(token_length=16):
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(token_length))
    return token

@app.route('/resetpasswd', methods = ['GET','POST'])
def resetpasswd():
    if request.method == 'POST':
        user_id = request.form['regi_id']
        user_name = request.form['regi_name']
        password1 = request.form['resetpassword']
        password2 = request.form['resetpassword2']

        connection = get_db()
        cursor = connection.cursor()

        if password1 == password2:
            password1 = hashlib.sha256(password1.encode('utf-8')).hexdigest()
            cursor.execute('UPDATE members SET passwd = ? WHERE id = ? AND name = ?', (password1, user_id, user_name,))
            connection.commit()
            cursor.close()
            flash("비밀번호 변경이 완료되었습니다")
            return redirect(url_for('index'))
        else:
            flash("비밀번호가 일치하지 않습니다")
            return render_template('resetpasswd.html')
    else:
        token = request.args.get('token')
        if token in temporary_tokens and time.time() < temporary_tokens[token]:
            return render_template('resetpasswd.html')
        else:
            flash('유효하지 않은 링크이거나 시간이 초과되었습니다')
            return render_template('findpasswd.html')

@app.route('/success/<username>', methods=['GET'])
def success(username):
    session['username'] = username
    page = request.args.get('page', 1, type=int)
    page_size = 10  # 한 페이지에 표시할 아이템 수
    offset = (page - 1) * page_size

    connection = get_db()
    cursor = connection.cursor()

    # 전체 데이터 수를 구합니다.
    cursor.execute("SELECT COUNT(*) FROM board")
    total_items = cursor.fetchone()[0]
    total_pages = (total_items + page_size - 1) // page_size

    # 게시글 목록을 역순으로 가져옵니다.
    cursor.execute("SELECT board.*, COUNT(comments.id) as answer_count FROM board LEFT JOIN comments ON board.num = comments.post_num GROUP BY board.num ORDER BY board.created DESC LIMIT ? OFFSET ?", (page_size, offset))
    question_list = cursor.fetchall()
    cursor.close()

    # 역순으로 번호를 매기지 않고, 정순으로 번호를 부여합니다.
    question_with_index = [(total_items - offset - idx, question) for idx, question in enumerate(question_list)]

    return render_template('success.html', name=username, question_list=question_with_index, current_page=page, total_pages=total_pages)

@app.route('/detail/<int:num>', methods = ['GET', 'POST'])
def detail(num):
    print(999)
    name = session.get('username')
    if request.method == 'POST':      
        print(0)       
        content = request.form['content']
        connection = get_db()
        cursor = connection.cursor()
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO comments (content, post_num, user, created) VALUES (?, ?, ?, ?)", (content, num, name, formatted_datetime))
        connection.commit()
        cursor.execute("SELECT * FROM board WHERE num = ?", (num,))
        question_data = cursor.fetchone()
        cursor.execute("SELECT * FROM comments WHERE post_num = ?", (num,))
        comments = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('question_detail.html', question = question_data, num = num, comments = comments, name = name)

    else:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM board WHERE num = ?", (num,))
        question_data = cursor.fetchone()
        cursor.execute("SELECT * FROM comments WHERE post_num = ?", (num,))
        comments = cursor.fetchall()
        cursor.close()
        return render_template('question_detail.html', question = question_data, num = num, comments = comments, name = name)

@app.route('/delete_comment/<int:num>/<string:id>')
def delete_comment(id, num):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM comments WHERE id = ?", (id,))
    connection.commit()
    connection.close()
    return redirect(url_for('detail', num = num))

@app.route('/delete_question/<int:num>/<string:id>')
def delete_question(id, num):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM board WHERE num = ?", (num,))
    cursor.execute("DELETE FROM comments WHERE post_num = ?", (num,))
    connection.commit()
    connection.close()
    return redirect(url_for('success', username = id))
@app.route('/update_question/<int:num>/<string:id>', methods=['GET', 'POST'])
def update_question(id, num):
    name = session.get('username')
    if request.method == 'POST':            
        content = request.form['content']
        title = request.form['title']
        current_datetime = datetime.datetime.now()
        created = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("UPDATE board SET title = ?, user = ?, created = ?, content = ? WHERE num = ?", (title, name, created, content, num))
        connection.commit()
        cursor.close()
        return redirect(url_for('detail', num=num))
    else:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM board WHERE num = ?", (num,))
        question_data = cursor.fetchone()
        cursor.close()
        return render_template('question_update.html',name = name, question = question_data)
@app.route('/create', methods = ['GET', 'POST'])
def question_create():
    name = session.get('username')
    if request.method == 'POST':            
        content = request.form['content']
        title = request.form['title']
        current_datetime = datetime.datetime.now()
        created = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO board (title, user, created, content) VALUES (?, ?, ?, ?)", (title, name, created, content))
        connection.commit()
        cursor.execute("SELECT * FROM board ORDER BY created DESC")
        question_data = cursor.fetchone()
        num = question_data['num']
        cursor.close()
        connection.close()
        return redirect(url_for('detail', num = num))

    return render_template('question_create.html', name = name)

if __name__ == '__main__':
    app.run(debug=True)
    