class parabola:
    #x is the tick direction
    #z is the note
    def __init__(self,msglist,x=0,y=32,z=0):    
        self.msglist = msglist
        self.x = x
        self.y = y
        self.z = z
        self.t = t

    def build(self):
        for msgs in self.msglist:
            for msg in msgs.msgs:
