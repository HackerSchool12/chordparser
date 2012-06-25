import redis
import pdb
from random import choice
import ast

def make_model(db, uchords):
    db.rpush( "chords", *uchords )

def next_chord(db, uch):
    '''uch lists UP TO 4 chords
    '''

    subl = map(str, uch[-4::])
    subs = set(subl)
    

    len_dbl = db.llen( "chords" )
    len_subl = len( subl )
    
#    pdb.set_trace()
    for e in range(0,len_dbl,len(subl)):
        elem = db.lindex("chords", e)
        if elem in subs:
            idx = subl.index( elem )
            candidate = db.lrange( "chords", e - idx, e + len_subl - idx - 1 )
            
            if subl == candidate :
                yield db.lindex("chords", e + len_subl - idx )
        
def rand_chord(db, uchords ):
    ch_list = list( next_chord( db, uchords ))
    rand = ast.literal_eval( choice( ch_list ) )
    return roman[ rand[0] ] + rand[1] 

def progression(db, start):
    while True:
        start = next_chord(db, start)
        yield start


roman = {
     0:"I",
     2:"ii",
     4:"iii",
     5:"IV",
     7:"V",
     9:"vi",
     11:"vii",
}

#r = redis.StrictRedis(host='localhost', port=6379, db=0)
