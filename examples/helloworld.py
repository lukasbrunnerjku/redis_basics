# pip install redis

# from source: python setup.py install

# https://redis.io/

import redis
import datetime


if __name__ == '__main__':

    r = redis.Redis()  # host='localhost', port=6379
    r.mset({"Croatia": "Zagreb", "Bahamas": "Nassau"})  # multi-set
    print(r.get("Bahamas"))  # b'Nassau'
    # .decode("utf-8")

    # redis keys have to be either string, int, float or byte
    today = datetime.date.today()
    stoday = str(today)
    visitors = {"dan", "jon", "alex"}
    # r.sadd(today, *visitors)  does not work
    r.sadd(stoday, *visitors)
    print(r.smembers(stoday), r.scard(stoday))
