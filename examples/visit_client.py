# The watcher’s goal is to monitor a stream of 
# IP addresses from multiple sources, keeping 
# an eye out for a flood of requests from a single 
# address within a suspiciously short amount of time.

import redis


r = redis.Redis(db=5)

r.lpush("ips", "51.218.112.236")
r.lpush("ips", "90.213.45.98")
r.lpush("ips", "115.215.230.176")
r.lpush("ips", "51.218.112.236")

for _ in range(20):
    r.lpush("ips", "104.174.118.18")
