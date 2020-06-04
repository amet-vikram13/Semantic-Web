import redis
import os


def get_connection():
    host = os.getenv("REDIS_HOST", "localhost")
    connection = redis.StrictRedis(host=host, port=6379, db=0)
    return connection
