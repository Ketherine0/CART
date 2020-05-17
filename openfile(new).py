def openFile(fileName):
    """ Open the file """
    rows = list()
    new_list = list()
    csvfile = open(fileName,'r', errors = "ignore")
    n = 1
    for strline in csvfile.readlines():
        if n == 1:
            n = 0
            continue
        else:
            strline = strline.replace('",','*')
            strline = strline.replace(',"','*')
            listline = strline.strip().split('*')
            for index, element in enumerate(listline):
                element = element.strip('"')
                new_list.append(element)
        # Exchange the "Rating" and "Android.Ver" to put the label in the last position
        new_list[2],new_list[-1] = new_list[-1],new_list[2]
        rows.append(new_list)
        new_list = []
    # Pop out the header
    rows.pop(0)
    return rows
