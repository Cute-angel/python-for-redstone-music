import mido

class msg:
    def __init__(self, t=0, T=0, c=0, n=0, v=0, l=1, p=0, program=0, control=0, value=0):
        self.tick     = t
        self.track    = T
        self.channel  = c
        self.note     = n
        self.velocity = v
        self.length   = l
        self.pitch    = p
        self.program  = program
        self.control  = control
        self.value    = value
        self.move     = []

class msgs:
    def __init__(self,msgs=None):
        self.msg = []
        if msgs != None:
            for msg in msgs:
                self.msg.append(msg)
        else:
            pass
    def load(self, newMsg):   
        self.msg.append(newMsg)

class Msglist:
    def load(midfile,tickrate=20):
        nowTime = 0.0
        mid = mido.MidiFile(midfile)
        for msg in mid:
            if msg.type == "note_on":
                