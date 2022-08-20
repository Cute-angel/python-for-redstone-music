class commander:
    def __init__(self,msgLists) -> None:
        self.msgLists = msgLists
    def initSequence(self):
        lens = []
        for  msgList in self.msgLists:
            # 添加 notelist 最后一项的note.tick
            lens.append(msgList.note_list[len(msgList.note_list)-1].tick)
        maxLenght = max(lens)
        return [[] for i in range(maxLenght+1)]
    def merge(*args) -> list:
        monList = []
        for i, arg in enumerate(args):
            if i == 0:
                monList = arg
            else:
                for i,l in enumerate(arg):
                    try:
                        monList[i] = monList[i] + l
                    except IndexError:
                        print("please use the same lenght seq")
                        raise IndexError
        return monList
    def contTicksPerSec(beatsPerMin) -> int:
        return beatsPerMin/3

class builder:
    #1 up 2 north 3 south 4 west 5 east 6 down
    # x-> east # z-> south
    #/setblock 0 64 1 minecraft:chain_command_block 0 replace {Command:"asf",auto:"1"}
    def __init__(self,seq,z0,y0) -> None:
        # this seq is cmd seq .total cmd
        self.seq = seq
        self.z0 = z0
        self.y0 = y0
        self.x = 0
        self.isDouble = True
    def buildInit(self):
        self.buildList = []
        if self.isDouble == True:
            for tick ,tickList in enumerate(self.seq):
                k = self.z0
                if tick % 2 == 0:
                    for cmd in tickList:
                        self.buildList.append(
                            f'setblock {tick} {self.y0} {k} minecraft:chain_command_block 2 replace {{Command:"{cmd}",auto:1}}'
                            )
                        k -= 1
                else:
                    for cmd in tickList:
                        self.buildList.append(
                            f'setblock {tick} {self.y0+1} {k} minecraft:chain_command_block 2 replace {{Command:"{cmd}",auto:1}}'
                        )
                        k -= 1
        return self.buildList
    
    def writeBuildList(self):
        buildList = self.buildInit()
        with open("./build.mcfunction","w") as mcfunction:
            for cmd in buildList:
                mcfunction.write(cmd+"\n")
    def writeBuildSeq(self):
        for tick , cmds in enumerate(self.seq):
            
            with open(f"./player/{tick}.mcfunction","w") as mcfunction:
                for cmd in cmds:
                    mcfunction.write(cmd+"\n")
                mcfunction.write(f"gamerule gameLoopFunction player:{tick+1}")
