from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
db_connect_string = os.getenv('DB_STR')

# Creating the engine.
engine = create_engine(db_connect_string, connect_args={"ca": "/etc/ssl/cert.pem"})


# Loads the tasks rendered in task-page.html given the user's id. (Returned as a list of dicts)
def load_tasks(ui):
    with engine.connect() as conn:
        result = conn.execute(text("select * from tasks where ui = :ui"), parameters=dict(ui=ui))
        ls_tasks = []
        for row in result:
            row_as_dict = row._mapping
            ls_tasks.append(row_as_dict)
        return ls_tasks


def load_tasks_by_priority(ui):
    with engine.connect() as conn:
        result = conn.execute(text("select * from tasks where ui = :ui ORDER BY priority ASC"), parameters=dict(ui=ui))
        ls_tasks = []
        for row in result:
            row_as_dict = row._mapping
            ls_tasks.append(row_as_dict)
        return ls_tasks


# Returns a task identified by its ID. Return type dict.
def load_task_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM tasks WHERE id = :val"), parameters=dict(val=id))
        rows = result.all()
        if len(rows) == 0:
            return None
        else:
            return rows[0]._mapping


# Deletes a task given its ID
def del_task(id):
    with engine.connect() as conn:
        result = conn.execute(text("DELETE FROM tasks WHERE id = :val"), parameters=dict(val=id))
        if result.rowcount == 0:
            return None


# Inserts a task given 'data' (via the HTML form in addnew.html)
def task_to_db(data, ui):
    with engine.connect() as conn:
        query = text("INSERT INTO tasks (title, the_task, priority, ui) VALUES (:title, :desc, :priority, :ui)")
        conn.execute(query, parameters=dict(title=data['title'], desc=data['the_task'], priority=data['Priority'],
                                            ui=ui))


# Adds new user and stores in database.
def new_user(username, hash_pswd):
    with engine.connect() as conn:
        query = text("INSERT INTO users (username, pswd) VALUES (:usr, :pwd)")
        conn.execute(query, parameters=dict(usr=username, pwd=hash_pswd))


# Retrieve a User Object given it's username
def get_userinfo_by_username(username):
    with engine.connect() as conn:
        query = text("SELECT * FROM users WHERE username = :un")
        result = conn.execute(query, parameters=dict(un=username))
        row = result.fetchone()
        if row:
            return dict(row._mapping)
        else:
            return None


# Function to check for duplicate user IDs; returns bool
def id_is_unique(username):
    with engine.connect() as conn:
        query = text("SELECT * FROM users WHERE username = :usrnme")
        result = conn.execute(query, parameters=dict(usrnme=username))
        return result.rowcount == 0


# Returns the ID # given a username as a str.
def get_userid_from_username(username):
    with engine.connect() as conn:
        query = text("SELECT id FROM users WHERE username = :usrnme")
        result = conn.execute(query, parameters=dict(usrnme=username))
        return str(result.fetchone())


def get_username_from_id(id):
    with engine.connect() as conn:
        query = text("SELECT username FROM users WHERE id = :id")
        result = conn.execute(query, parameters=dict(id=id))
        name = result.fetchone()
        return str(name[0])
