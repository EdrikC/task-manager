from flask import Flask, render_template, request
from database import load_tasks, task_to_db, del_task

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/task-page')
def add_task():
    return render_template('task-page.html', tsk=load_tasks())


@app.route('/task-page/confirmed', methods=['post'])
def confirmed_tsk():
    data = request.form
    task_to_db(data)
    return render_template('task-page.html', tsk=load_tasks())


@app.route('/task-page/del', methods=['post'])
def delete_task():
    data = request.form
    tsk_id = data.get('id')
    del_task(tsk_id)
    return render_template('task-page.html', tsk=load_tasks())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
