import redis
import chordmodel
from random import randrange
from ast import literal_eval
from random import choice

r = redis.StrictRedis(host='localhost', port=6379, db=0)

l = r.llen("chords")
pattern = [literal_eval(r.lindex("chords", randrange(0, l)))]

try:
    while True:
        pattern.append(
                literal_eval(
                    choice(
                        list(
                            chordmodel.next_chord(r, pattern)))))
except:
    pass

for i in pattern:
    print chordmodel.roman[ i[0] ] + i[1], 
