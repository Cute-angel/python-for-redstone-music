def single2many(start,end):
    firstp = start
    secondp = end       #this is a list
    finlist = []
    for point in secondp:
        finlist.append((firstp,point))
    return finlist

def many2many(start,end):
    firstp,secondp = start,end          #all is list
    finlist = []
    for p1 in firstp:
        for p2 in secondp:
            finlist.append((p1,p2))
    return finlist
