class Node:
    """ Node stores feature column, feature value, and some data """
    def __init__(self, value = None, col = None, left = None, right = None, result = None, data = None, wrong = 0):
        # index of feature
        self.col = col  
        # split value of feature
        self.value = value 
        # left branch: True or larger than value
        self.left = left 
        # right branch: False or smaller than value
        self.right = right 
        # if it is leave node, result will be a dictionay which stores the numbers of each label
        self.result = result
        # if it is leave node, data will be a list which stores the dataset
        self.data = data # if it is the last 
        # error rate of each node
        self.wrong = wrong

def openFile(fileName):
    """ Open the file """
    rows = list()
    new_list = list()
    csvfile = open(fileName,'r', errors = "ignore")
    for strline in csvfile.readlines():
        # Manipulate the "Installs" feature
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

def divData(rows, col, value):
    """ Divide Data according to value """
    # set1: left branch dataset
    set1 = list()
    # set2: right branch dataset
    set2 = list()
    # Traverse every row in the given dataset
    for row in rows:
        # If split value is number, transfer the feature value to number and compare with split feature value
        if isinstance(value, int) or isinstance(value, float):
            # Use try-except to manipulate string value like "NA" and "varies with devices"
            try:
                # Feature "Reviews"
                if col == 3:
                    i = eval(row[col])
                # Feature "Size"
                elif col == 4:
                    i = eval(row[col].strip("MK"))
                # Feature "Price"
                elif col == 7:
                    i = eval(row[col].lstrip("$"))
                # if feature value is larger than split feature value, add row to left branch
                if i > value:
                    set1.append(row)
                # Otherwise, add row to right branch
                else:
                    set2.append(row)
            except:
                pass # whether to ???
        # If split value is string, compare it with feature value
        else:
            # if feature value is equal to split feature value, add row to left branch
            if row[col] == value:
                set1.append(row)
            # Otherwise, add row to right branch
            else:
                set2.append(row)
    return set1, set2

def countLabel(rows):
    """ Count the number of data with each label """
    result = {}
    result[True] = 0
    result[False] = 0
    for row in rows:
        # Use try-except to pass invalid label like "NA"
        try:
            result[eval(row[-1]) > 4.5] += 1
        except:
            pass # whether??????
    return result

def Gini(rows):
    """ Compute Gini index """
    # im is impurity
    im = 0
    row_length = len(rows)
    counts = countLabel(rows)
    if row_length == 0:
        return 1
    # Compute impurity
    for label in counts:
        im += (counts[label] / row_length) * (counts[label] / row_length)
    gini = 1 - im
    return gini

def divValue(rows, col):
    """ Get all feature splitting value in train datasets """
    # col_value stores all feature splitting value
    col_value = list()
    # pre_value and extra_col_value stores number value and other values
    pre_value = set()
    extra_col_value = list()
    # If split value is string, use set to store unrepeated split values 
    if col in [1,2,5,6,8,9,10,11]:
        col_value = list(set(row[col] for row in rows))
    # If split value is number, transfer the feature value to number
    else:
        for row in rows:
            # Use try-except to manipulate string value, like "varies with devices"
            try:
                # Feature "Reviews"
                if col == 3:
                    pre_value.add(eval(row[col]))
                # Feature "Size"
                elif col == 4:
                    pre_value.add(eval(row[col].strip("MK")))
                # Feature "Price"
                elif col == 7:
                    pre_value.add(eval(row[col].lstrip("$")))
            except:
                extra_col_value.append(row[col])
        # Transfer set to list and sort the list
        pre_value = sorted(list(pre_value))
        # Compute the mean value of every two values in pre_value list as feature splitting value
        for i in range(len(pre_value)-1):
            col_value.append((pre_value[i] + pre_value[i+1]) / 2)
            # Merge extra_col_value to col_value
        col_value += extra_col_value
    return col_value

def createTree(rows, isUsed = [False]*13):
    """ Create CART Tree """
    if len(rows) == 0:
        print("empty node")
        return Node()
    # Current gini index
    current_gain = Gini(rows)
    column_length = len(rows[0])
    row_length = len(rows)
    # Minimum gini index indicate largest in Information
    best_gain = 0.0
    best_set = None
    # best_criteria include column of feature and value.
    best_criteria = None
    # Traverse all features except the name and label.
    for col in range(1, column_length-1):
        # If the feature has not been used, use it.
        if isUsed[col] is False:
            # Get all split values.
            col_value = divValue(rows, col)
            # Traverse all split values.
            for value in col_value:
                # Divide data to two sets according to split value.
                set1, set2 = divData(rows, col, value)
                # p is the proportion of set1.
                p = len(set1) / row_length
                # gain is the Information Gain
                gain = current_gain - p * Gini(set1) - (1-p) * Gini(set2)
                # If this split value could get larger information gain, apply it.
                if gain > best_gain:
                    best_criteria = (col, value)
                    best_gain = gain
                    best_set = (set1, set2)
    # If the information gain larger than 0, use recursion to continue to split.
    if best_gain > 0:
        isUsed[best_criteria[0]] = True
        # Left branch continue to create tree
        left = createTree(best_set[0], isUsed.copy())
        # Right branch continue to create tree
        right = createTree(best_set[1], isUsed.copy())
        # Compute the error rate
        wrong = left.wrong + right.wrong 
        # Create Node
        return Node(value = best_criteria[1], col = best_criteria[0], left = left, right = right, wrong = wrong)
    # If the information gain is smaller than 0, stop creating tree and create a leave node.
    else:
        result = countLabel(rows)
        # Small is the number of wrong label
        small = result[True]
        if result[False] < small:
            small = result[False]
        wrong = small / total_len
        # Create leave Node
        return Node(result = result, data = rows, wrong = wrong)

def test(data, tree):
    """ Test one piece of data """
    # If it is not a leave node, check feature value to continue testing
    if tree.result is None:
        col = tree.col
        value = tree.value
        try:
            # Feature "Reviews"
            if col == 3:
                candi = eval(data[col]) 
            # Feature "Size"
            elif col == 4:
                candi = eval(data[col].strip("MK"))
            # Feature "Price"
            elif col == 7:
                candi = eval(data[col].lstrip("$"))
            # If it is a string, keep it string
            else:
                candi = data[col]
        # if the value in 3,4 or 7 columns is string, keep it string
        except:
            candi = data[col]
        # If feature split value is number, compare with number
        if isinstance(value, int) or isinstance(value, float):
            # If the value is string, add to left branch
            if type(candi) == str:
                result = test(data, tree.left)
            # If the value is larger than split value, add to left branch
            elif candi > value:
                result = test(data, tree.left)
            # If the value is smaller than split value, add to right branch
            else:
                result = test(data, tree.right)
        # If feature split value is string, compare with string
        else:
            # If the value equals to split value, add to left branch
            if candi == value:
                result = test(data, tree.left)
            # Otherwise, add to right branch
            else:
                result = test(data, tree.right)
        return result
    # If it is a leave node, return the result
    else:
        true = tree.result[True]
        false = tree.result[False]
        # Major label is the result
        if true >= false:
            return True
        else:
            return False

def finalTest(datasets, tree):
    """ Test datasets """
    # Compute the correctness and errors
    correct = 0
    fault = 0
    for data in datasets:
        result = test(data, tree)
        # Use try-except to manipulate chaos label
        try:
            # Check the answer: the correct label
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

rows = openFile("train.csv")
total_len = len(rows[:6072])
my_tree = createTree(rows[:6072])
print(my_tree)
print("wrong rate: ", my_tree.wrong)
datasets = openFile("test.csv")
accuracy = finalTest(datasets, my_tree)
print(accuracy)