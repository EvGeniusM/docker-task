import os
import socket

from flask import Flask, request

app = Flask(__name__)

VERSION = "1.0"
DATA_DIR = os.environ.get("DATA_DIR", "data")
NOTE_FILE = os.path.join(DATA_DIR, "note.txt")


@app.get("/")
def index():
    return f"Hello from Docker! version={VERSION} host={socket.gethostname()}\n"


@app.get("/health")
def health():
    return "Finally ok again\n"


@app.get("/write")
def write():
    text = request.args.get("text", "hello")
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(NOTE_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    return f"Saved to {NOTE_FILE}: {text}\n"


@app.get("/read")
def read():
    if not os.path.exists(NOTE_FILE):
        return "no note yet\n", 404
    with open(NOTE_FILE, encoding="utf-8") as f:
        return f"{f.read()} (Read by {socket.gethostname()})\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
