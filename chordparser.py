import re
import sys
from operator import add

chord_re = re.compile(r"\b([A-Ga-g][b#]?)(m)?((?:maj)?[0-9])?(sus[0-9])?(/[A-G][b#]?)?\s")


if( len( sys.argv ) > 1 ):
    text = open( sys.argv[1] )
   
def parse(file):
    for line in file:
        for chord in chord_re.findall(line):
            chord = list(chord)
            chord[0] = chord[0].capitalize()
            yield chord

number = {
    "A":0,
    "A#":1,
    "Bb":1,
    "B":2,
    "B#":3,
    "Cb":2,
    "C":3,
    "C#":4,
    "Db":4,
    "D":5,
    "D#":6,
    "Eb":6,
    "E":7,
    "E#":8,
    "Fb":7,
    "F":8,
    "F#":9,
    "Gb":9,
    "G":10,
    "G#":11,
    "Ab":11,
}

roman = {
     0:"I",
     2:"ii",
     4:"iii",
     5:"IV",
     7:"V",
     9:"vi",
     11:"vii",
}

chords = dict((v,k) for k, v in number.iteritems())

def minor(ch):
    return ch[0] - 1, ch[1]

def major7th(ch):
    return [ch[1], 11]

def minor7th(ch):
    return [ch[1], 10]

pressed = [False for i in range(12)]

def noteify(chord):
    root = number[ chord[0] ]
    quality = [4, 7]  
    if chord[1] == 'm':
        quality = minor( quality )
    if chord[2] == 'maj7':
        quality = major7th( quality )
    if chord[2] == '7':
        quality = minor7th( quality )

    return root, root+quality[0], root+quality[1]

def track_notes(ch):
    for n in ch:
        pressed[n%12] = True

major_scale = [2,2,1,2,2,2,1]

def reductions(f, init, l):
    yield init
    for v in l:
        init = f(init, v)
        yield init

scales = []
for root in range(12):
    scale = reductions(add, root, major_scale)
    scale = set([n%12 for n in scale])
    scales.append(scale)

def convert_scale(pressed):
    for i, n in zip(range(12), pressed):
        if n:
            yield i

def convert_universal( key, ch ):
    return number[ ch[0] ] - key


if __name__ == "__main__":
    file = list(parse( open (sys.argv[1] ) ))
    for n in file:
        track_notes(noteify(n))

    s = set( convert_scale( pressed ))
    key = None

    for i, scale in enumerate(scales):
        if s.issubset(scale):
            key = i
            print chords[i] + " Major"
            break
    
    for n in file:
        print roman[convert_universal( key, n )]