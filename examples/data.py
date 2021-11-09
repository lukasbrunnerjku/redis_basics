import redis
import json
from pprintpp import pprint


r = redis.Redis()

restaurant_484272 = {
    "name": "Ravagh",
    "type": "Persian",
    "address": {
        "street": {
            "line1": "11 E 30th St",
            "line2": "APT 1",
        },  # that will not work
        "city": "New York",
        "state": "NY",
        "zip": 10016,
    }
}

# redis.exceptions.DataError: Invalid input of type: 'dict'.
# Convert to a bytes, string, int or float first.
#r.hmset(484272, restaurant_484272)

# workaround - serialization ie. json.dumps()
r.set(484272, json.dumps(restaurant_484272))
pprint(json.loads(r.get(484272)))

# workaround - compression
import bz2

blob = "i have a lot to talk about" * 10000
print(len(blob.encode("utf-8")))

# Set the compressed string as value
r.set("msg:500", bz2.compress(blob.encode("utf-8")))
print(len(r.get("msg:500")))
print('Magnitude of savings', 260_000 / 122)

# Get and decompress the value, then confirm it's equal to the original
rblob = bz2.decompress(r.get("msg:500")).decode("utf-8")
rblob == blob

# The way that serialization and compression are 
# related here is that they all occur client-side.
