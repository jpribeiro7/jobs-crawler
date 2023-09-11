import redis
from redis import from_url

# Create a redis client
redisClient = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Push URLs to Redis Queue
redisClient.lpush('jobs_queue:start_urls', "https://textkernel.careers/jobs")