import os
import socket

import psycopg
import redis
from flask import Flask, request

app = Flask(__name__)

VERSION = "1.0"
DATABASE_URL = os.environ["DATABASE_URL"]
cache = redis.Redis.from_url(os.environ["REDIS_URL"], socket_connect_timeout=2)


def get_conn():
    conn = psycopg.connect(DATABASE_URL)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS notes (id INT PRIMARY KEY, text TEXT NOT NULL)"
    )
    conn.commit()
    return conn


@app.get("/")
def index():
    return f"Hello from Docker! version={VERSION} host={socket.gethostname()}\n"


@app.get("/health")
def health():
    return "ok\n"


@app.get("/db/write")
def db_write():
    text = request.args.get("text", "hello")
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO notes (id, text) VALUES (1, %s) "
            "ON CONFLICT (id) DO UPDATE SET text = EXCLUDED.text",
            (text,),
        )
    return f"Saved to db: {text}\n"


@app.get("/db/read")
def db_read():
    with get_conn() as conn:
        row = conn.execute("SELECT text FROM notes WHERE id = 1").fetchone()
    if row is None:
        return "no note in db yet\n", 404
    return f"{row[0]} (Read by {socket.gethostname()})\n"


@app.get("/hits")
def hits():
    n = cache.incr("hits")
    return f"hits={n} (Read by {socket.gethostname()})\n"