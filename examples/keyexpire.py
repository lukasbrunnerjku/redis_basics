import redis
from datetime import timedelta
import time

r = redis.Redis()

# setex: "SET" with expiration
r.setex(
    "runner",
    timedelta(minutes=1),
    value="now you see me, now you don't"
)

print(r.ttl("runner"))  # "Time To Live", in seconds
print(r.pttl("runner"))  # Like ttl, but milliseconds

r.expire("runner", timedelta(seconds=3))  # set new expire window
time.sleep(3.2)
print(r.get("runner"))
print(r.exists("runner"))  # Key & value are both gone (expired)
