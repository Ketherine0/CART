import csv
# Data info: features including numbers,date,strings

class Node:
    """ Node stores feature and feature value """
    def __init__(self, value = None, col = None, left = None, right = None, result = None, data = None, wrong = 0, leave = 0, alpha = 0, kini = 0, current = None):
        self.col = col # index of feature 
        self.value = value # true value
        self.left = left # True
        self.right = right # False
        self.result = result # if it's the last then result
        self.data = data # if it is the last 
        self.wrong = wrong
        self.kini = kini
        self.leave = leave
        self.alpha = alpha
        self.current = current
    def pop(self):
        self.leave = self.leave - self.left.leave - self.right.leave
        self.result = self.current
        self.wrong = self.kini
        self.left.leave = 0
        self.right.leave = 0
    def copy(self):
        copy = Node()
        copy.col = self.col  # index of feature 
        copy.value = self.value 
        copy.left = self.left # True
        copy.right = self.right # False
        copy.result =self.result # if it's the last then result
        copy.data = self.data # if it is the last 
        copy.wrong = self.wrong
        copy.kini = self.kini
        copy.leave = self.leave
        copy.alpha = self.alpha
        copy.current = self.current
        return copy


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
        current = countLabel(rows)
        small = current[True]
        if current[False] < small:
            small = current[False]
        kini = small / total_len
        wrong = left.wrong + right.wrong 
        # print(best_criteria, wrong)
        return Node(value = best_criteria[1], col = best_criteria[0], left = left, right = right, wrong = wrong, current = current, kini = kini)
    else:
        result = countLabel(rows)
        small = result[True]
        if result[False] < small:
            small = result[False]
        wrong = small / total_len
        # print(countLabel(rows),wrong)
        return Node(result = result, data = rows, wrong = wrong, current = result, kini = wrong)

def isLeaf(tree):
    if tree.result:
        return True
    else:
        return False

def calcTt(tree):
    if isLeaf(tree):
        return 1
    tree.leave = calcTt(tree.left) + calcTt(tree.right)
    return tree.leave

def calcAlphaList(tree):
    if isLeaf(tree):
        return
    costNotSplit = tree.kini
    costSplit = tree.wrong
    alpha = (costNotSplit-costSplit)/(tree.leave-1)
    tree.alpha = alpha
    if alpha < calcAlphaList.best_alpha:
        calcAlphaList.best_alpha = alpha
    calcAlphaList(tree.left)
    calcAlphaList(tree.right)

def cut(tree, alpha):
    if isLeaf(tree):
        return 
    if tree.alpha == alpha:
        tree.pop()
    else:
        cut(tree.left, alpha)
        cut(tree.right, alpha)

def pruning(tree): # actually it's node
    i = 0
    print ('i=',i,tree)
    tree_list = []
    while not isLeaf(tree):
        calcTt(tree)
        calcAlphaList.best_alpha = 100
        calcAlphaList(tree)
        i += 1
        print('i=',i,'alpha',calcAlphaList.best_alpha)
        cut(tree, calcAlphaList.best_alpha)
        tree_list.append(tree.copy())
        print(tree)
    return tree_list

def validation(validation, tree_list):
    best_tree = None
    best_accuracy = 0
    accuracy_list = list()
    for tree in tree_list:
        accuracy = final_test(validation, tree)
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_tree = tree
        accuracy_list.append(accuracy)
    return best_tree, best_accuracy, accuracy_list

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

def final_test(datasets, tree):
    correct = 0
    fault = 0
    for data in datasets:
        result = test(data, tree)
        try:
            if eval(data[-1]) > 4.5:
                answer = True
            else:
                answer = False
            if answer ==  result:
                correct += 1
            else:
                fault += 1
        except:
            pass
    accuracy = correct / (correct + fault) * 100
    return accuracy

# def openFile(fileName):
#     rows = list()
#     csvfile = open(fileName,'r', errors = "ignore")
#     for line in csvfile.readlines():
#         line = line.strip().split(',')
#         for index, element in enumerate(line):
#             line[index] = element.strip('"')
#         line[2],line[-1] = line[-1],line[2]
#         rows.append(line)
#     rows.pop(0)
#     return rows

# rows = openFile("train.csv")

with open("train.csv",'r',errors = "ignore") as handle:
    lines = csv.reader(handle)
    rows = list()
    for line in lines:
        line[2],line[-1] = line[-1],line[2]
        rows.append(line)
    rows.pop(0)

total_len = len(rows[:6072])
my_tree = createTree(rows[:6072])
print(my_tree)
print("wrong rate: ", my_tree.wrong)
with open("test.csv",'r',errors = "ignore") as handle:
    lines = csv.reader(handle)
    datasets = list()
    for line in lines:
        line[2],line[-1] = line[-1],line[2]
        datasets.append(line)
    datasets.pop(0)

accuracy = final_test(datasets, my_tree)
print("The original final accuracy is :", accuracy)
tree_list = pruning(my_tree)
print("they are trees:", tree_list)
for tree in tree_list:
    print(tree.leave)
    print(tree.wrong)
best_tree, best_accuracy, accuracy_list = validation(rows[6072:], tree_list)
print("THe best tree:", best_tree, best_accuracy)
print(accuracy_list)
accuracy = final_test(datasets,best_tree)
print("The final accuracy is :", accuracy)