import random
from pprintpp import pprint
import logging
import redis

logging.basicConfig()

class OutOfStockError(Exception):
    """Raised when PyHats.com is all out of today's hottest hat"""

def buyitem(r: redis.Redis, itemid: int) -> None:
    with r.pipeline() as pipe:
        error_count = 0
        while True:
            try:
                # Get available inventory, watching for changes
                # related to this itemid before the transaction,
                pipe.watch(itemid)
                nleft: bytes = r.hget(itemid, "quantity")

                # !!!
                # if changes happen to the watched data entry between
                # the hget and the hincrby commands redis will
                # throw a WatchError

                if nleft > b"0":
                    # buffer all of the commands into one, and 
                    # then send them to the server in a single request
                    pipe.multi()  # a transaction has no real time response
                    # to the individual commands since they return all simultaneously 
                    pipe.hincrby(itemid, "quantity", -1)
                    pipe.hincrby(itemid, "npurchased", 1)
                    pipe.execute()  # get the sequence of results back all at once
                    break
                else:
                    # Stop watching the itemid and raise to break out
                    pipe.unwatch()
                    raise OutOfStockError(
                        f"Sorry, {itemid} is out of stock!"
                    )
            except redis.WatchError:
                # Log total num. of errors by this user to buy this item,
                # then try the same process again of WATCH/HGET/MULTI/EXEC
                error_count += 1
                logging.warning(
                    "WatchError #%d: %s; retrying",
                    error_count, itemid
                )
    return None


if __name__ == '__main__':
    random.seed(444)
    hats = {f"hat:{random.getrandbits(32)}": i for i in (
        {
            "color": "black",
            "price": 49.99,
            "style": "fitted",
            "quantity": 1000,
            "npurchased": 0,
        },
        {
            "color": "maroon",
            "price": 59.99,
            "style": "hipster",
            "quantity": 500,
            "npurchased": 0,
        },
        {
            "color": "green",
            "price": 99.99,
            "style": "baseball",
            "quantity": 200,
            "npurchased": 0,
        })
    }

    r = redis.Redis(db=1)

    # write data into redis, a pipe.hmset() is more efficient 
    # than 3x r.hmset() because they are sent at once
    with r.pipeline() as pipe:
        for h_id, hat in hats.items():
            pipe.hmset(h_id, hat)  # hash multi-set
        pipe.execute()

    print(r.keys())  # careful: O(N)

    pprint(r.hgetall("hat:56854717"))  # pretty print

    # increase quantity and npurchased by -1 and 1 respectivly
    r.hincrby("hat:56854717", "quantity", -1)
    r.hincrby("hat:56854717", "npurchased", 1)
    # others: INCR, INCRBY, INCRBYFLOAT, ZINCRBY, and HINCRBYFLOAT

    print(r.hget("hat:56854717", "quantity"))  # 199

    buyitem(r, "hat:56854717")
    buyitem(r, "hat:56854717")
    buyitem(r, "hat:56854717")
    print(r.hmget("hat:56854717", "quantity", "npurchased"))

    for _ in range(196):
        buyitem(r, "hat:56854717")
    print(r.hmget("hat:56854717", "quantity", "npurchased"))

    buyitem(r, "hat:56854717")
