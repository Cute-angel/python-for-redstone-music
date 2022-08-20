import mido

from player import Player
from utils import builder
from utils import commander
from effect import soma

midfile = mido.MidiFile("./1.mid")
tracks = midfile.tracks

# 1 beat = 20 gt


ticksPerBeat = midfile.ticks_per_beat
beatsPerMinute = 85

Msglists = []

toFind = []

def findNote(type,msg,ct,notelist):
    global toFind
    global ticksPerBeat
    if type == "on":
        toFind.append(note(msg.note,int(round(ct/ticksPerBeat*20)),msg.velocity))
    if type == "off":
        for i , Note in enumerate(toFind):
            if msg.note == Note.note:
                if ct/ticksPerBeat - Note.tick/20 > 1:
                    
                    Note.p = ""
                    notelist.append(Note)
                else:
                    
                    Note.p = "c"
                    notelist.append(Note)
                del toFind[i]

class note:
    def __init__(self,n,t,v) -> None:
        self.note = n
        self.tick = t
        self.velocity = v / 127
        self.p = ""

class Msglist:
    # 通道 乐器
    def __init__(self,channel,program=1,noteList=None) -> None:
        if noteList is None:
            self.note_list = []
        else:
            self.note_list = noteList
        self.channel = channel 
        self.program = program


for i,track in enumerate(tracks):
    currentTick = 0
    msglist = Msglist(i,program=1)
    for msg in track:
        currentTick = currentTick + msg.time
        if msg.is_meta:
            pass
        else:
            if msg.type == "program_change":
                Msglist.program = msg.program + 1
            if msg.type == 'note_on':
                gt = currentTick / ticksPerBeat * 20 
                if gt - int(round(gt)) < 0 or gt - int(round(gt)) > 0:
                    print(f'warning gt is {gt}')
                # add to tofind list when it turn off it will write to Msglist
                findNote("on",msg,currentTick,msglist.note_list)
            if msg.type == "note_off":
                findNote("off",msg,currentTick,msglist.note_list)
    if len(msglist.note_list) > 0:
        Msglists.append(msglist)
                
cPlayer = Player(Msglists)
cEffect = soma(Msglists,1)
b= cEffect.load()
a = cPlayer.load()

finalList = commander.merge(a,b)
build = builder(finalList,-5,64)
build.writeBuildList()

print()
