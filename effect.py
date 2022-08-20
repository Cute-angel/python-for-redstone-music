import math

from utils import commander

class soma(commander):
    lastLine = None
    direct = 1
    def __init__(self,msgLists,track) -> None:
        self.msgList = msgLists[track] #指定轨道
        self.track = track
        self.msgLists = msgLists
        self.r = 0
        self.g = 1
        self.b = 1

        self.lastLine = None
        self.direct = 1
        # this is the mult tracks data
        # it cant be changed
    class Line():
        def __init__(self,x1,x2,z1,z2) -> None:
            self.x1 = x1
            self.x2 = x2
            self.z1 = z1
            self.z2 = z2
            if self.z1 == self.z2:
                self.k = (self.x2-self.x1)/0.0000000000000000000000000000000000000000000000000000000000000000000000000000001
            else:
                self.k = (self.x2-self.x1)/(self.z2-self.z1)
            self.b = self.x1 - self.k * self.z1
        def makeLenght(self):
            return math.sqrt((self.x1-self.x2)**2+(self.z1-self.z2)**2)
    class crossPoint():
        def __init__(self,line1,line2) -> None:
            if line1.k == line2.k:
                self.x = None
                self.z = None
            else:
                self.z = (line2.b-line1.b)/(line1.k-line2.k)
                self.x = line1.k * self.z + line1.b
    class perpendicularBisector(Line):
        def __init__(self, x1, x2, z1, z2) -> None:
            super().__init__(x1, x2, z1, z2)
            self.k = -1 / self.k
            #计算中点
            self.xM = (self.x1+self.x2)/2
            self.zM = (self.z1+self.z2)/2
            self.b = self.xM - self.k * self.zM
    
    def init(self):     #for one to mult prepare 
        res = []        # 二维list
        pointList = self.initSequence()
        for note in self.msgList.note_list:
            pointList[int(note.tick)].append(note)
        for noteList in pointList:
            if len(noteList) == 0:
                pass
            else:
                res.append(noteList)
        return res

    def updateDirect(self,direct,rX,x):
        if rX > x:
            return direct * -1
        else:
            return direct
    def updateDegree(self,d1,d2):
        #d1 sin d2 cos to pi ~ -pi
        if d1 > 0 and d2 < math.pi/2:
            return d1
        if d1 > 0 and d2 > math.pi/2:
            return math.pi - d1
        if d1 < 0 and d2 < math.pi/2:
            return  d1 * -1
        if d1 < 0 and d2 > math.pi/2:
            return -math.pi - d1
    def load(self):
        pointList = self.init()
        # 当初始是lastline 为none 在之后中lastline 要被依次刷新
        #lastLine = None
        self.buildList = self.initSequence()
        #保存最终生成的list
        #direct = 1
        #设定初始方向 1 为 顺时针


        # 只处理一对一的函数 
        # 一对多使用for循环处理
        def load(thisNote,nextNote,num,isUpdateLastLine):
            # 全局变量

            x = float(thisNote.tick)
            z = float(thisNote.note)
            nextX = float(nextNote.tick)
            nextZ = float(nextNote.note)
            if num == 0:        #num = 0 时 特殊处理 lastline 为 none
                line = self.Line(x,nextX,z,nextZ)
                if isUpdateLastLine:
                    self.lastLine = line         #fresh lastLine
                # 圆心
                rX = (x+nextX)/2
                rZ = (z+nextZ)/2
                r = line.makeLenght()/2
                # asin() -> -pi/2 ~ pi/2
                d1 = math.asin((x-rX)/r)
                nextD1 = math.asin((nextX-rX)/r)
                d2 = math.acos((z-rZ)/r)
                nextD2 = math.acos((nextZ-rZ)/r)
                d = self.updateDegree(d1,d2)
                nextD = self.updateDegree(nextD1,nextD2)
                tickLenght = nextX - x
                #cpt = 100 / tickLenght
                if self.direct == 1:
                    k = (nextD - d)/tickLenght # >0
                    cmd = f"particleex tickparameter endRod {rX} 64 {rZ} 0 1 1 0 240 0 0 0 0 {tickLenght} x,z={r}*sin({d}+{k}*t),{r}*cos({d}+{k}*t) 0.1 10 {int(tickLenght)}"
                    self.buildList[int(x)].append(cmd)
                else:
                    nextD = nextD - math.pi*2    # <0
                    k = (nextD-d)/tickLenght
                    cmd = f"particleex tickparameter endRod {rX} 64 {rZ} 0 1 1 0 240 0 0 0 0 {tickLenght} x,z={r}*sin({d}+{k}*t),{r}*cos({d}+{k}*t) 0.1 10 {int(tickLenght)}"
                    self.buildList[int(x)].append(cmd)

            else:
                # 计算圆心
                line = self.perpendicularBisector(x,nextX,z,nextZ)
                cp = self.crossPoint(self.lastLine,line)
                rX = cp.x
                rZ = cp.z

                line = self.Line(rX,nextX,rZ,nextZ)
                r = line.makeLenght()
                # 更新lastline
                if isUpdateLastLine: 
                    self.lastLine = line
                # 更新方向
                self.direct = self.updateDirect(self.direct,rX,x)
                # 返回正确的弧度 pi ~ -pi
                d1 = math.asin((x-rX)/r)
                nextD1 = math.asin((nextX-rX)/r)
                d2 = math.acos((z-rZ)/r)
                nextD2 = math.acos((nextZ-rZ)/r)
                d = self.updateDegree(d1,d2)
                nextD = self.updateDegree(nextD1,nextD2)

                tickLenght = nextX - x
                if self.direct == 1:
                    k = (nextD-d)/tickLenght
                    cmd = f"particleex tickparameter endRod {rX} 64 {rZ} 0 1 1 0 240 0 0 0 0 100 x,z={r}*sin({d}+{k}*t),{r}*cos({d}+{k}*t) 0.1 10 {int(tickLenght)}"
                    self.buildList[int(x)].append(cmd)
                else:
                    nextD = nextD - math.pi * 2
                    k = (nextD - d)/tickLenght
                    cmd = f"particleex tickparameter endRod {rX} 64 {rZ} 0 1 1 0 240 0 0 0 0 100 x,z={r}*sin({d}+{k}*t),{r}*cos({d}+{k}*t) 0.1 10 {int(tickLenght)}"
                    self.buildList[int(x)].append(cmd)

        for num ,noteList in enumerate(pointList[0:len(pointList)-1]):
            for index ,thisNote in enumerate(noteList):
                if index == 0:      #只处理第一个
                    for i,nextNote in enumerate(pointList[num+1]):
                        if i == 0:      #只保存第一个的lastline
                            load(thisNote,nextNote,num,True)
                        else:
                            load(thisNote,nextNote,num,False)
                else:
                    pass
        return self.buildList

class redstoneBlock(commander):
    def __init__(self, msgLists) -> None:
        super().__init__(msgLists)
    def load(self):
        buildList = self.initSequence()