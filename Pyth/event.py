import eventlet
from eventlet import wsgi
import datetime
import redis
from urllib.parse import urlparse
from flask import Flask
from redis.connection import SSLConnection

eventlet.monkey_patch()

class SSLRedisConnection(SSLConnection):
    def __init__(self, *args, **kwargs):
        kwargs['ssl_cert_reqs'] = None  # Set to the appropriate value based on your needs
        super().__init__(*args, **kwargs)

my_application = Flask(__name__)

REDIS_URL = "http://pbe6272829f62aa1f18c6ee4f8f55456aa71d044a75ca069a3b5f6b6963971b56@ec2-46-137-49-233.eu-west-1.compute.amazonaws.com:27779/"
print("REDIS_URL: ", REDIS_URL)

url_parts = urlparse(REDIS_URL)
host = url_parts.hostname
port = url_parts.port
password = url_parts.password

try:
    pool = redis.ConnectionPool(
        host=host,
        port=port,
        password=password,
        connection_class=SSLRedisConnection,
        decode_responses=True
    )

    my_application.redis = redis.Redis(connection_pool=pool)
    my_application.redis.set("redis", "ready")
except Exception as e:
    print(f"Error: {e}")

@my_application.route("/")
def index():
    my_application.redis.set("hello", str(datetime.datetime.now()))
    return "Hello, World!"

if __name__ == "__main__":
    # Use eventlet's WSGI server directly
    wsgi.server(eventlet.listen(('0.0.0.0', 5000)), my_application)
