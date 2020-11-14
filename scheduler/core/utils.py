import logging
import psycopg2
import time
from functools import wraps
from urllib.parse import urlparse


def connect_db(uri):
    u = urlparse(uri)
    user, password = (u.username, u.password)
    dbname, host, port = (u.path[1:], u.hostname, u.port)
    return psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)


def time_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        time_start = time.time()
        func(*args, **kwargs)
        duration = round(time.time() - time_start, 5)
        logging.info(f"Task: {func.__name__} completed in {duration}s")

    return wrapper