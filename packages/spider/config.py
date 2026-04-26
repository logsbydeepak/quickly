import os

import psycopg
import redis

import db


def init_db():
    url = os.getenv("DB_URL")

    if not url:
        raise Exception("Missing DB_URL")

    conn = psycopg.connect(url)

    return conn


def init_redis():
    redis_url = os.getenv("REDIS_URL")

    if not redis_url:
        raise Exception("Missing REDIS_URL")

    return redis.Redis.from_url(redis_url)
