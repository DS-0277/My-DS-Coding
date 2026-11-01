import os
import socket

from flask import Flask, jsonify

app = Flask(__name__)
server_id = os.environ.get("SERVER_ID", socket.gethostname())


@app.get("/")
def home():
    return jsonify(
        message="Hello from the backend application",
        server_id=server_id,
        hostname=socket.gethostname(),
    )


@app.get("/healthz")
def healthz():
    return jsonify(status="healthy", server_id=server_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
