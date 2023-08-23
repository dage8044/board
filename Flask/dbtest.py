import os
import sqlite3
from flask import Flask, request, redirect

app = Flask(__name__)

# 데이터베이스 파일 경로
current_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_directory, "database.db")

def get_db():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 딕셔너리 형태로 데이터 사용 가능
    return conn

def template(contents, content, id=None):
    contextUI = ''
    if id is not None:
        contextUI = f'''
            <li><a href="/update/{id}/">update</a></li>
            <li><form action="/delete/{id}/" method="POST"><input type="submit" value="delete"></form></li>
        '''
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create/">create</a></li>
                {contextUI}
            </ul>
        </body>
    </html>
    '''

def get_contents_from_db():
    conn = get_db()
    cursor = conn.execute('SELECT * FROM topics')
    topics = cursor.fetchall()
    conn.close()
    return topics

def get_contents():
    topics = get_contents_from_db()
    contents = ''
    for topic in topics:
        contents += f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return contents

@app.route('/')
def index():
    return template(get_contents(), '<h2>Welcome</h2>Hello, WEB')

@app.route('/read/<int:id>/')
def read(id):
    conn = get_db()
    cursor = conn.execute('SELECT * FROM topics WHERE id = ?', (id,))
    topic = cursor.fetchone()
    conn.close()
    if topic is not None:
        return template(get_contents(), f'<h2>{topic["title"]}</h2>{topic["body"]}', id)
    return 'Topic not found!', 404

@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return template(get_contents(), content)
    elif request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        conn = get_db()
        cursor = conn.execute('INSERT INTO topics (title, body) VALUES (?, ?)', (title, body))
        conn.commit()
        conn.close()
        return redirect('/')

@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    conn = get_db()
    cursor = conn.execute('SELECT * FROM topics WHERE id = ?', (id,))
    topic = cursor.fetchone()
    
    if request.method == 'GET':
        if topic is not None:
            content = f'''
                <form action="/update/{id}/" method="POST">
                    <p><input type="text" name="title" placeholder="title" value="{topic["title"]}"></p>
                    <p><textarea name="body" placeholder="body">{topic["body"]}</textarea></p>
                    <p><input type="submit" value="update"></p>
                </form>
            '''
            conn.close()
            return template(get_contents(), content, id)
        return 'Topic not found!', 404
    elif request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        cursor = conn.execute('UPDATE topics SET title=?, body=? WHERE id=?', (title, body, id))
        conn.commit()
        conn.close()
        return redirect(f'/read/{id}/')

@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    conn = get_db()
    cursor = conn.execute('DELETE FROM topics WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
