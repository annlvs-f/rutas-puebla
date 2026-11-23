import os

import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

if not REDIS_URL:
    raise RuntimeError(
        "Falta la variable REDIS_URL. Crea un archivo .env con tu cadena de "
        "conexión de Redis Cloud (ver README)."
    )

redis_client = redis.from_url(REDIS_URL, decode_responses=True)


def probar_conexion() -> bool:
    try:
        return bool(redis_client.ping())
    except redis.exceptions.RedisError:
        return False
