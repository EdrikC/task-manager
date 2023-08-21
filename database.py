from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os


load_dotenv()
db_connect_string = os.getenv('DB_STR')


# Creating the engine.
engine = create_engine(db_connect_string, connect_args={
    "ssl": {
        "ca": "/etc/ssl/cert.pem",
    }
})


def load_tasks():
    with engine.connect() as conn:
        result = conn.execute(text("select * from tasks"))
        ls_tasks = []
        for row in result:
            row_as_dict = row._mapping
            ls_tasks.append(row_as_dict)
        return ls_tasks


def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM tasks WHERE id = :val"), parameters=dict(val=id))
        rows = result.all()
        if len(rows) == 0:
            return None
        else:
            return rows[0]._mapping


def del_task(id):
    with engine.connect() as conn:
        result = conn.execute(text("DELETE FROM tasks WHERE id = :val"), parameters=dict(val=id))
        if result.rowcount == 0:
            return None


def task_to_db(data):
    with engine.connect() as conn:
        query = text("INSERT INTO tasks (title, the_task, priority) VALUES (:title, :desc, :priority)")
        conn.execute(query, parameters=dict(title=data['title'], desc=data['the_task'], priority=data['Priority']))

