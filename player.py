from utils import commander

class Player(commander):
    def load(self) -> list:
        playList = self.initSequence() # 生成二维列表
        for msgList in self.msgLists:
            for note in msgList.note_list:
                playList[note.tick].append(
                    f"execute @p ~ ~ ~ playsound {msgList.program}{note.p}.{note.note} voice @p ~ ~ ~ {note.velocity}"
                )
        return playList