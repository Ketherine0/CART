import csv
from math import log
# Data info: features including numbers,date,strings

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

rows = openFile('train.csv')

class Node:
    """ Node stores feature and feature value """
    def __init__(self, value = None, col = None, left = None, right = None, result = None, data = None, wrong = 0):
        self.col = col # index of feature 
        self.value = value # true value
        self.left = left # True
        self.right = right # False
        self.result = result # if it's the last then result
        self.data = data # if it is the last 
        self.wrong = wrong

def divData(rows, col, value): # rows are data; col is number col of feature; value is 分类标准
    """ Divide Data according to value """
    set1 = list()
    set2 = list()
    for row in rows:
        if isinstance(value, int) or isinstance(value, float):
            try:
                if col == 3:
                    i = eval(row[col])
                elif col == 4:
                    i = eval(row[col].strip("MK"))
                elif col == 7:
                    i = eval(row[col].lstrip("$"))
                if i > value:
                    set1.append(row)
                else:
                    set2.append(row)
            except:
                pass
        else:
            if row[col] == value:
                set1.append(row)
            else:
                set2.append(row)
    # different standards
    return set1, set2

def countLabel(rows):
    """ Count the label to compute Gini """
    result = {}
    result[True] = 0
    result[False] = 0
    for row in rows:
        try:
            result[eval(row[-1]) > 4.5] += 1
        except:
            pass
    return result

def Gini(rows):
    """ Compute Gini """
    im = 0
    row_length = len(rows)
    counts = countLabel(rows)
    if row_length == 0:
        return 1
    for label in counts:
        im += (counts[label] / row_length) * (counts[label] / row_length)
    gini = 1 - im
    return gini

def divValue(rows, col):
    """ divide data according to feature """
    col_value = list()
    pre_value = set()
    extra_col_value = list()
    if col in [1,2,5,6,8,9,10,11]:
        col_value = list(set(row[col] for row in rows))
    else:
        for row in rows:
            # for reviews, eval()
            try:
                if col == 3:
                    pre_value.add(eval(row[col]))
                # for size, strip "M" or "K"
                elif col == 4:
                    pre_value.add(eval(row[col].strip("MK")))
                # for price, strip "$"
                elif col == 7:
                    pre_value.add(eval(row[col].lstrip("$")))
            except:
                extra_col_value.append(row[col])
        pre_value = sorted(list(pre_value))
        for i in range(len(pre_value)-1):
            col_value.append((pre_value[i] + pre_value[i+1]) / 2)
        col_value += extra_col_value
    return col_value

def createTree(rows, isUsed = [False]*13):
    """ Recursive function """
    if len(rows) == 0:
        print("empty node")
        return Node()
    current_gain = Gini(rows)
    column_length = len(rows[0])
    row_length = len(rows)
    global best_gain
    best_gain = 0.0
    best_set = None
    best_criteria = None
    # traverse all features, except name and label
    for col in range(1, column_length-1):
        if isUsed[col] is False:
            # get all feature values
            col_value = divValue(rows, col)
            # traverse all feature values
            for value in col_value:
                # divide data
                set1, set2 = divData(rows, col, value)
                p = len(set1) / row_length
                gain = current_gain - p * Gini(set1) - (1-p) * Gini(set2)
                if gain > best_gain:
                    best_criteria = (col, value)
                    best_gain = gain
                    best_set = (set1, set2)
    if best_gain > 0:
        isUsed[best_criteria[0]] = True
        left = createTree(best_set[0], isUsed.copy())
        right = createTree(best_set[1], isUsed.copy())
        wrong = left.wrong + right.wrong 
        print(best_criteria, wrong)
        return Node(value = best_criteria[1], col = best_criteria[0], left = left, right = right, wrong = wrong)
    else:
        result = countLabel(rows)
        small = result[True]
        if result[False] < small:
            small = result[False]
        wrong = small / total_len
        print(countLabel(rows),wrong)
        return Node(result = countLabel(rows), data = rows, wrong = wrong)

# e.g.:Shoot Hunter-Gun Killer,GAME,4.3,320334,27M,"50,000,000+",Free,0,Teen,Action,8-Aug-18,1.1.2,4.1 and up
# e.g.: [name,category,Android.Ver,Reviews,Size,Installs,Type,Price,Content.Rating,Genres,Last.Updated,Current.Ver,Rating]
total_len = len(rows[:10])
my_tree = createTree(rows[:10])
print(my_tree)
print("wrong rate: ", my_tree.wrong)


with open("test.csv", "r", errors = "ignore") as new_handle:
    lines = csv.reader(new_handle)
    reads = list()
    for line in lines:
        line[2],line[-1] = line[-1],line[2]
        reads.append(line)
    reads.pop(0)

def test(data, tree):
    if tree.result is None:
        col = tree.col
        value = tree.value
        try:
            if col == 3:
                candi = eval(data[col]) 
            # for size, strip "M" or "K"
            elif col == 4:
                candi = eval(data[col].strip("MK"))
            # for price, strip "$"
            elif col == 7:
                candi = eval(data[col].lstrip("$"))
            else:
                candi = data[col]
        except:
            candi = data[col]
        if isinstance(value, int) or isinstance(value, float):
            if type(candi) == str:
                result = test(data, tree.left)
            elif candi > value:
                result = test(data, tree.left)
            else:
                result = test(data, tree.right)
        else:
            if candi == value:
                result = test(data, tree.left)
            else:
                result = test(data, tree.right)
        return result
    else:
        true = tree.result[True]
        false = tree.result[False]
        if true >= false:
            return True
        else:
            return False
correct = 0
fault = 0
for data in reads:
    result = test(data, my_tree)
    try:
        if eval(data[-1]) > 4.5:
            answer = True
        else:
            answer = False
        if answer ==  result:
            correct += 1
            # print("correct")
        else:
            fault += 1
            # print("wrong")
    except:
        pass
accuracy = correct / (correct + fault) * 100
print(correct, fault)
print("The accuracy is ", accuracy)
    
def entropy(rows):
    result = countLabel(rows)
    entro = 0
    for i in result:
        if float(result[i]) != 0:
            pro = float(result[i]) / len(rows)
            entro -= pro * (log(pro)/log(2))
    return entro

def cut(decision_tree, best_gain, data):
    
    if decision_tree.left.result == None:
        cut(decision_tree.left, best_gain, data)
    if decision_tree.right.result == None:
        cut(decision_tree.right, best_gain, data)
    
    if decision_tree.left.result != None:
        if decision_tree.right.result != None:
            left_brunch = []
            right_brunch = []

            for TorF, count in decision_tree.left.result.items():
                left_brunch.extend([[TorF]]*count)
            for TorF, count in decision_tree.right.result.items():   
                right_brunch.extend([[TorF]]*count)

            pro = float(len(left_brunch)/len(left_brunch+right_brunch))
            current_gain = entropy(left_brunch+right_brunch) - pro * entropy(left_brunch) - (1-pro) *entropy(right_brunch)
            if current_gain < best_gain:
                decision_tree.left = None
                decision_tree.right = None
                decision_tree.result = countLabel(left_brunch+right_brunch)

    return decision_tree


decision_tree = cut(my_tree, best_gain, reads)
print(decision_tree)


def test_prune(decision_tree, rows):
    global reads
    reads = rows 
    pr_correct = 0
    pr_fault = 0
    for data in reads:
        if data[decision_tree.col] == decision_tree.value:
            if decision_tree.value == data[-1]:
                pr_correct += 1
                reads.pop(reads.index(data))
            else:
                pr_fault += 1
                reads.pop(reads.index(data))

        if decision_tree.left.result == None:
            test_prune(decision_tree.left, reads)
        if decision_tree.right.result == None:
            test_prune(decision_tree.right, reads)
        if len(reads) == 0:
            return pr_correct, pr_fault

if len(reads) > 0:
    pr_correct, pr_fault = test_prune(decision_tree, reads)
accuracy = pr_correct / (pr_correct + pr_fault)


correct = 0
fault = 0
for data in reads:
    result = test(data, decision_tree)
    try:
        if eval(data[-1]) > 4.5:
            answer = True
        else:
            answer = False
        if answer ==  result:
            correct += 1
            print("correct")
        else:
            fault += 1
            print("wrong")
    except:
        pass
accuracy = correct / (correct + fault) * 100
print(correct, fault)
print("The accuracy after pruning is ", accuracy)
    


