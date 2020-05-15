import csv
from itertools import combinations

train_file = 'train.csv'
train_data = []
with open(train_file) as csvfile:
    csv_reader = csv.reader(csvfile)
    train_header = next(csv_reader)
    for row in csv_reader:
        train_data.append(row)

train_data = [[x for x in row] for row in train_data]


def variable(train_data):
    global app_label
    global real_rating
    app_label = []
    real_rating = []
    for features in train_data:
        app_label.append(features[0])
        real_rating.append(features[2])
        features.remove(features[0])
        features.remove(features[1])

# print(train_data[:])

def features_com(features):
    combinations_list = []
    for i in range(1,len(features)):
        pos_combinations = list(combinations(features, len(features[0:i])))
        combinations_list.extend(pos_combinations)
    features_combinations = zip(combinations_list[0:int(len(combinations_list)/2)], combinations_list[len(combinations_list)-1:int(len(combinations_list)/2)-1:-1])
    return features_combinations

def gini_index(data):
    less, larger = data
    gini = 1
    for less_value in less:
        pro = len(less) / (len(less)+len(larger))
        gini -= pro ** 2
    for larger_value in larger:
        pro = len(larger) / (len(less)+len(larger))
        gini -= pro ** 2
    return gini
    

def split_data(data_list, column, value):
    less_list = []
    larger_list = []
    
    for i in range(len(data_list)):
        if data_list[i][column] in value:
            if float(real_rating[i]) <= 4.5:
                less_list.append(data_list[i][column])
            else:
                larger_list.append(data_list[i][column])
    
    return less_list, larger_list


def choose_features(data_list):
    choose_feature_index = 0
    choose_split = None
    gini_max = 1

    for i in range(len(data_list[0])-1):
        feature_list = []
        unique_feature = []
        
        feature_list = [features[i] for features in data_list]
        unique_feature = list(set(feature_list))
        
        for split in features_com(unique_feature):
            gini_gain = 0
            if len(split) == 1:
                continue

            left, right = split
            left_list = []
            right_list = []
            left_list = split_data(data_list, i, left)
            right_list = split_data(data_list, i, right)

            left_pro = float(len(left_list[0]+left_list[1]) / len(feature_list))
            right_pro = float(len(right_list[0]+right_list[1]) / len(feature_list))
            gini_gain += left_pro * gini_index(left_list)
            gini_gain += right_pro * gini_index(right_list)

            if gini_gain <= gini_max:
                gini_max = gini_gain
                choose_feature_index = i
                choose_split = left_list, right_list     
    return choose_feature_index, choose_split



def tree(data_list, features_label):
    
    best_feature_index, best_split = choose_features(data_list)
    best_feature = features_label[best_feature_index]

    if best_feature_index == -1:
        rating_count={}

        for rating in real_rating:

            # how to improve?
            if rating not in rating_count.keys(): 
                rating_count[rating] = 0
            rating_count[rating] += 1

        sorted_rating_count = sorted(rating_count.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sorted_rating_count[0][0]

    decision_tree = {best_feature:{}}
    best_feature_values = [rows[best_feature_index] for rows in data_list]
    best_feature_values = list(set(best_feature_values))

    best_split = best_split[0][0]+best_split[0][1], best_split[1][0]+best_split[1][1]
    for value in best_split:
        if len(value) <= 1:
            del(features_label[best_feature_index])
        decision_tree[best_feature][value] = tree(split_data(data_list, best_feature_index, value), features_label)

    return decision_tree


variable(train_data[:5])
# print(train_data[:5])
my_tree = tree(train_data[:5], train_header)
print(my_tree)
