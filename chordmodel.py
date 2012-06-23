import redis
from random import randrange


def make_model(db, uchords):
    prev = ''
    for ch in uchords:
        db.rpush(prev, ch)
        prev = ch

def next_chord(db, uch):
    l = db.llen(uch)
    return db.lindex(uch, randrange(0, l))

def progression(db, start):
    while True:
        start = next_chord(db, start)
        yield start


#r = redis.StrictRedis(host='localhost', port=6379, db=0)
