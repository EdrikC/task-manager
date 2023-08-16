from flask import Flask, render_template
from database import load_tasks, del_task


app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/task-page')
def add_task():
    return render_template('task-page.html', tsk=load_tasks())


@app.route('/task-page')
def delete_task(id):
    return render_template('task-page.html', tsk=del_task(id))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
