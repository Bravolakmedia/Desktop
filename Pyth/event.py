import eventlet
import datetime
import redis
import numpy as np
from urllib.parse import urlparse
from flask import Flask

eventlet.monkey_patch()

my_application = Flask(__name__)

REDIS_URL = "***********************"
print("REDIS_URL: ", REDIS_URL)

url_parts = urlparse(REDIS_URL)
host = url_parts.hostname
port = url_parts.port
password = url_parts.password

try:
    # Use an eventlet-friendly Redis connection pool for async support
    pool = redis.ConnectionPool(
        host=host,
        port=port,
        password=password,
        ssl_cert_reqs=None,  # Adjust this based on your requirements
        decode_responses=True  # Decode responses to UTF-8 for Flask
    )

    my_application.redis = redis.Redis(connection_pool=pool)

    my_application.redis.set("redis", "ready")
except Exception as e:
    print(f"Error: {e}")

@my_application.route("/")
def index():
    # Set a value in Redis
    my_application.redis.set("hello", str(datetime.datetime.now()))
    return "Hello, World!"

if __name__ == "__main__":
    # Use eventlet's WSGI server instead of Flask's default server
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), my_application)
