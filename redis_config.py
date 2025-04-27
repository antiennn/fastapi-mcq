import os
from dotenv import load_dotenv
import redis

# 1. Load biến môi trường từ .env
load_dotenv()

# 2. Lấy thông tin Redis từ env
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT
)

