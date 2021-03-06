# flaskというフレームワークからFlaskをインポート
from flask import Flask, render_template, request, redirect
import sqlite3

# appというflaskアプリを作る的な宣言。
app = Flask(__name__)


@app.route('/')
def helloworld():
    return "Hello World."


@app.route('/<name>')
def greet(name):
    return name + "こんにちは"


@app.route('/template')
def template():
    py_name = "材木座くん"
    return render_template('index.html', name=py_name)


@app.route('/weather')
def weather():
    py_weather = "Sunny"
    return render_template('base.html', weather=py_weather)


@app.route('/dbtest')
def dbtest():
    # flasktest.dbに接続
    conn = sqlite3.connect('flasktest.db')
    # 中身が見られるようにしている
    c = conn.cursor()
    # SQL文の実行
    c.execute("select name, age, address from users")
    # 取ってきたレコードを格納
    user_info = c.fetchone()
    # データベース接続終了
    c.close()

    print(user_info)
    return render_template('dbtest.html', user_info=user_info)


@app.route('/add', methods=["GET"])
def add_get():
    return render_template('add.html')


@app.route('/add', methods=["POST"])
def add_post():
    # フォームのtaskに入力されたデータを取得
    task = request.form.get("task")

    # DBと接続
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute("insert into task values(null, ?)", (task, ))
    # 変更を確定する
    conn.commit()
    conn.close()
    return redirect('/list')


@app.route('/list')
def task_list():
    user_name = "大将くん"
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute("select id, task from task")
    task_list = []
    for row in c.fetchall():
        task_list.append({"id": row[0], "task": row[1]})
    c.close()
    return render_template(
        'tasklist.html',
        task_list=task_list,
        user_name=user_name)

    # flaskが持っている開発用のサーバーを起動する。
if __name__ == '__main__':
    app.run(debug=True)
