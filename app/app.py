import os
import socket

import redis
from flask import Flask, jsonify

app = Flask(__name__)

# Settings come from environment variables (no secrets in the code)
APP_NAME = os.getenv("APP_NAME", "Docker Visit Counter")
REDIS_HOST = os.getenv("REDIS_HOST", "cache")

cache = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)


@app.route("/")
def index():
    visits = cache.incr("visits")  # add 1 to the counter stored in Redis
    return jsonify(app=APP_NAME, visits=visits, served_by=socket.gethostname())


@app.route("/health")
def health():
    try:
        cache.ping()  # is Redis reachable?
        return jsonify(status="ok"), 200
    except Exception as exc:
        return jsonify(status="unhealthy", error=str(exc)), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
