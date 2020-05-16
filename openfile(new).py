def openFile(fileName):
    rows = list()
    newlist = list()
    csvfile = open(fileName,'r', encoding='UTF-8')
    for strline in csvfile.readlines():
        strline = strline.replace('",','*')
        strline = strline.replace(',"','*')
        listline = strline.strip().split('*')
        for index, element in enumerate(listline):
            element = element.strip('"')
            newlist.append(element)
        newlist[2],newlist[-1] = newlist[-1],newlist[2]
        rows.append(newlist)
        newlist = []
    rows.pop(0)
    print(rows[0])
    return rows
