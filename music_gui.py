from Tkinter import *
from functools import partial
from mingus.midi import fluidsynth
import mingus.core.progressions as progressions
from mingus.containers import NoteContainer
from mingus.containers.Track import Track
from chordmodel import *
from mingus.midi import MidiFileOut
import tkFileDialog

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
        
	self.sug_var = StringVar()
	self.sug_label = Label( master, textvariable = self.sug_var).pack()	

    #### Chord Buttons ####
        for ch in roman_num:
            
            btn = Button(frame, text=roman[ch], foreground="SystemMenuActiveText", command=partial( self.print_ch, ch ) )
            btn.pack(side=LEFT)
            
            self.buttons[ ch ] = btn 
            
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
         
    #### Callbacks #### 
    def print_ch( self, ch ):
        mod = ''
	mod = mod + ('M' if self.maj_var.get() else '')
        mod = mod + ('7' if self.add7_var.get() else '')
        
	self.progression.append(( ch, mod ))
		
	uprog = [ roman[ch[0]] + ch[1] for ch in self.progression ]

        self.prog_var.set( '  '.join( uprog ) )
        print ch

    def pop_ch( self ):
        self.progression.pop()
	uprog = [ roman[ch[0]] + ch[1] for ch in self.progression ]
        self.prog_var.set( '  '.join( uprog ) )
        
    def play_prog( self ):
	uprog = [ roman[ch[0]] + ch[1] for ch in self.progression ]
	ch = progressions.to_chords(uprog, "C")
	nc = map(NoteContainer, ch)

	t = Track()
	for chord in nc:
	    t.add_notes(chord)
	fluidsynth.play_Track(t)

    def save_midi( self ):
	file_name = tkFileDialog.asksaveasfilename()
	uprog = [ roman[ch[0]] + ch[1] for ch in self.progression ]
	ch = progressions.to_chords(uprog, "C")
	nc = map(NoteContainer, ch)

	t = Track()
	for chord in nc:
	    t.add_notes(chord)
	MidiFileOut.write_Track( file_name,t)

    def suggest( self ):
	uprog = [ roman[ ch[0]] + ch[1] for ch in next_chord( self.progression )]
	concise =  frequencies( uprog )
	self.sug_var.set( '  '.join(["%s: %s" % (k, v) for k, v in concise.iteritems()]  ))
	
	
def frequencies( chords ):
    initial = {}
    for ch in chords:
	value = initial.setdefault( ch, 0 )
	initial[ ch ] = value + 1
    return initial
	





root = Tk()

app = App(root)

root.mainloop()
