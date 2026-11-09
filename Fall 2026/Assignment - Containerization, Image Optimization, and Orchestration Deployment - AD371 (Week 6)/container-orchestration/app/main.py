import os
import time
from flask import Flask, jsonify


app = Flask(__name__)
START_TIME = time.monotonic()


@app.get("/")
def home():
    return """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Containerized Web Application</title>
  </head>
  <body>
    <main>
      <h1>Containerized Web Application</h1>
      <p>The application is running successfully.</p>
      <p>Container hostname: <strong id="hostname">loading...</strong></p>
      <p>Uptime: <strong id="uptime">loading...</strong> seconds</p>
    </main>
    <script>
      fetch('/runtime')
        .then(response => response.json())
        .then(data => {
          document.querySelector('#hostname').textContent = data.hostname;
          document.querySelector('#uptime').textContent = data.uptime_seconds;
        });
    </script>
  </body>
</html>"""


@app.get("/healthz")
def healthz():
    return jsonify({"status": "healthy"}), 200


@app.get("/runtime")
def runtime():
    return jsonify(
        {
            "application": "containerized-web-application",
            "hostname": os.uname().nodename,
            "uptime_seconds": round(time.monotonic() - START_TIME, 2),
        }
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
