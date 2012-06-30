from random import choice
import pickle
import pdb

with open("data") as f:
     data = pickle.load( f )


def next_chord( uch ):
    ''' Takes list of UP TO 4 chords.
        Generate the next chord in the series based on the data set.
    '''

    subl = uch[-4::]
    subs = set(subl)
    

    len_data = len( data )
    len_subl = len( subl )
   
   
#    pdb.set_trace()
    for e in range(0,len_data,len_subl):
        elem = data[e]
        if elem in subs:       
            idx = subl.index( elem )
            candidate = data[e - idx : e + len_subl - idx ]
            
            if subl == candidate :
             #   pdb.set_trace()
                try:
                    yield data[ e + len_subl - idx ]
                except IndexError:
                    pass    
#r = redis.StrictRedis(host='localhost', port=6379, db=0)
