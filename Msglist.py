import mido

class msg:
    def __init__(self, k=0, t=0, T=0, c=0, n=0, v=0, l=1, p=0, program=0, control=0, value=0):
        self.type     = k
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
    def __init__(self,tick,msgs=None):
        self.msgs = []
        self.tick = tick
        if msgs != None:
            for msg in msgs:
                self.msg.append(msg)
        else:
            pass
    def append(self, newMsg):   
        self.msgs.append(newMsg)

class Msglist:
    __Msglist = []
    def makelength(self):
        for msgs in self.__Msglist:
            stick = msgs.tick
            for msg in msgs:
                if msg.type !== "note_on":
                    continue
                note = msg.note
                channel = msg.channel
                track = msg.track

    def findByTick(self,tick):
        for Msgs in self.__Msglist:
            if Msgs.tick == tick:
                return Msgs
        newmsgs = msgs(tick)
        __Msglist.append(newmsgs)
        return newmsgs
    def load(midfile,tickrate=20):
        nowTime = 0.0
        mid = mido.MidiFile(midfile)
        for msg in mid:
            if msg.type == "note_on":
                if msg.time > 0:
                    nowTime += msg.time
                tick = round(nowTime*tickrate)
                msgs = self.findByTick(tick)
                msg = msg("note_on",tick,msg.track,msg.channel,msg.note,msg.velocity)
                msgs.append(msg)
            elif msg.type == "note_off"
                if msg.time > 0:
                    nowTime += msg.time
                tick = round(nowTime*tickrate)
                msgs = self.findByTick(tick)
                msg = msg("note_off",tick,msg.track,msg.channel,msg.note,msg.velocity)
                msgs.append(msg)
            elif msg.is_meta:
                if msg.time > 0:
                    nowTime += msg.time
            else:
                if msg.time > 0:
                    nowTime += msg.time