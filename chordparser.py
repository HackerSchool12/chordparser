import re
import sys
from operator import add, and_
from itertools import takewhile, imap

chord_re = re.compile(r">([A-Ga-g][b#]?)(m)?((?:maj)?[0-9])?(sus[0-9]|add[0-9])?(/[A-Ga-g][b#]?)?<")
text_line = re.compile(r"(^[aA] \w|\w a \w)")

def parse(file):
    for line in file:
        if not text_line.search(line):
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

def track_notes(pressed, ch):
    for n in ch:
        pressed[n%12] += 1

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
    for i, n in enumerate(pressed):
        if n:
            yield i

def convert_universal( key, ch ):
    return (number[ ch[0] ] - key) % 12, ch[2]

def ask_key(default=''):
    i = raw_input("In which key?[%s]: " % default)
    if i == '':
        i = default

    if i == '':
        raise KeyError("no key")

    return number[i]

def get_key(pressed):
    keys = []
    s = set( convert_scale( pressed ))

    for i, scale in enumerate(scales):
        if s.issubset(scale):
            keys.append(i)

    if not keys:
        key = ask_key()
    elif len(keys) > 1:
        key = ask_key(chords[keys[0]])
    else:
        key = keys[0]

    return key

def get_universal(f):
    pressed = [0] * 12
    with open(f) as source:
        chords = list(parse(source))

    for n in chords:
        track_notes(pressed, noteify(n))

    key = get_key(pressed)

    for n in chords:
        yield convert_universal(key, n)

if __name__ == "__main__":
    for uni in get_universal(sys.argv[1]):
        print roman[uni[0]], uni[1]
