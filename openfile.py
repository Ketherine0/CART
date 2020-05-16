def openFile(fileName):
    rows = list()
    csvfile = open(fileName,'r', encoding='UTF-8')
    for line in csvfile.readlines():
        line = line.strip().split(',')
        for index, element in enumerate(line):
            line[index] = element.strip('"')
        line[2],line[-1] = line[-1],line[2]
        rows.append(line)
    rows.pop(0)
    return rows
# 啊啊啊list index out of range
