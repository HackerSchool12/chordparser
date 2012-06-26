from mingus.midi import fluidsynth
import mingus.core.progressions as progressions
from mingus.containers import NoteContainer
from mingus.containers.Track import Track
import sys

fluidsynth.init(sys.argv[1])

pro = sys.stdin.read().split()

ch = progressions.to_chords(pro, "C")

nc = map(NoteContainer, ch)

t = Track()

for chord in nc:
    t.add_notes(chord)

fluidsynth.play_Track(t)

