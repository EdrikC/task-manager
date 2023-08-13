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
