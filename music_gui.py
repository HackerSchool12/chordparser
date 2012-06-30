from Tkinter import *
from functools import partial
from mingus.midi import fluidsynth
import mingus.core.progressions as progressions
from mingus.containers import NoteContainer
from mingus.containers.Track import Track
from chordmodel import *
from mingus.midi import MidiFileOut
import tkFileDialog
from chordparser import number

roman = {
     0:"I",
     2:"ii",
     4:"iii",
     5:"IV",
     7:"V",
     9:"vi",
     11:"vii",
}

class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()
       
	fluidsynth.init("ChoriumRevA.SF2")

        roman_num = [0,2,4,5,7,9,11]

        self.progression = []
        self.buttons = {}
        
        self.prog_var = StringVar()
        self.display = Label( master, textvariable = self.prog_var).pack()
        
        self.uniprog_var = StringVar()
        self.unidisplay = Label( master, textvariable = self.uniprog_var).pack()

	self.sug_var = StringVar()
	self.sug_label = Label( master, textvariable = self.sug_var).pack()	

    #### Chord Buttons ####
         
	self.key_btn = Listbox(frame)
        self.key_btn.bind("<<ListboxSelect>>", self.display_progression)
	self.key_btn.pack(side=BOTTOM)
        for k in number.keys():
            self.key_btn.insert(END, k)

        for ch in roman_num:
            
            btn = Button(frame, text=roman[ch], foreground="SystemMenuActiveText", command=partial( self.print_ch, ch ) )
            btn.pack(side=LEFT)
            
            self.buttons[ ch ] = btn 

    #### other buttons ####
            
        self.pop = Button(frame, text='Del', foreground="#FF0000", background="#00FF00", command=self.pop_ch)
        self.pop.pack(side=BOTTOM)

	self.play = Button(frame, text='Play', foreground="black", command=self.play_prog)
	self.play.pack(side=TOP)

	self.sugg = Button(frame, text='?', fg="blue", command=self.suggest)
	self.sugg.pack(side=BOTTOM)	

	self.save_btn = Button(frame, text='Save', command=self.save_midi)
	self.save_btn.pack(side=TOP)

    #### Checkbox buttons for intervals ####
        self.add7_var = BooleanVar()
        self.add7 = Checkbutton( master, text="+ 7", variable = self.add7_var )
        self.add7.pack()

        self.maj_var = BooleanVar()
        self.maj = Checkbutton( master, text="Major", variable = self.maj_var )
        self.maj.pack()

    def get_key(self):
        try:
            sel = map(int, self.key_btn.curselection())
            print sel
            return number.keys()[sel[0]]
        except IndexError:
            return 'C'

    def get_progression(self, prog):
	return [ roman[ch[0]] + ch[1] for ch in prog ]

    def display_progression(self, nop=None):
        s = []
        pr = self.get_progression(self.progression)
        for ch in progressions.to_chords(pr, self.get_key()):
            c = NoteContainer(ch)
            s.append(c.determine(True)[0])

        self.prog_var.set( '  '.join( s ) )
        self.uniprog_var.set('  '.join( pr ))
    
    #### Callbacks #### 
    def print_ch( self, ch ):
        ''' Append chord and modifier to progressioni and print updated progression to terminal.
        '''
        mod = ''
	mod = mod + ('M' if self.maj_var.get() else '')
        mod = mod + ('7' if self.add7_var.get() else '')
        
	self.progression.append(( ch, mod ))

        self.display_progression()
        print ch

    def pop_ch( self ):
        ''' Pop last chord off progression list.
        '''
        self.progression.pop()
        self.display_progression()
        
    def play_prog( self ):
        ''' Saves chords to track and plays using fluidsynth.
        '''
	ch = progressions.to_chords(self.get_progression(self.progression), self.get_key())
	nc = map(NoteContainer, ch)

	t = Track()
	for chord in nc:
	    t.add_notes(chord)
	fluidsynth.play_Track(t)

    def save_midi( self ):
        '''Opens save dialog, converts progression list to chords in track, saves track midi.
        '''
	file_name = tkFileDialog.asksaveasfilename()
	ch = progressions.to_chords(self.get_progression(self.progression), self.get_key())
	nc = map(NoteContainer, ch)

	t = Track()
	for chord in nc:
	    t.add_notes(chord)
	MidiFileOut.write_Track( file_name,t)

    def suggest( self ):
        '''Combines list of unique suggestions and save in sug_var (which displays as label)
        '''
	concise =  frequencies( self.get_progression(next_chord(self.progression)) )
	self.sug_var.set( '  '.join(["%s: %s" % (k, v) for k, v in concise.iteritems()]  ))
	
	
def frequencies( chords ):
'''Tracks frequency of unique chords and returns a dictionary of the chord (universal notation) and its count.
'''    
    initial = {}
    for ch in chords:
	value = initial.setdefault( ch, 0 )
	initial[ ch ] = value + 1
    return initial
	





root = Tk()

app = App(root)

root.mainloop()
