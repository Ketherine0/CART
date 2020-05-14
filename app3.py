import csv
from itertools import combinations
import numpy as np
import random

train_file = 'train.csv'
train_data = []
with open(train_file) as csvfile:
    csv_reader = csv.reader(csvfile)
    train_header = next(csv_reader)
    for row in csv_reader:
        train_data.append(row)

train_data = [[x for x in row] for row in train_data]

real_rating = []
features_label = []
for features in train_data:
    features_label.append(features[0])
    real_rating.append(features[2])
    features.remove(features[0])
    features.remove(features[2])

train_data = np.array(train_data)
train_header = np.array(train_header)
# print(train_data.shape)
# print(train_header.shape)
print(train_data[:])

def features_com(features):
    combinations_list = []
    for i in range(1,len(train_data)+1):
        pos_combinations = list(combinations(features, len(features[0:i])))
        combinations_list.extend(pos_combinations)
    features_combinations = zip(combinations_list[0:int(len(combinations_list)/2)], combinations_list[len(combinations_list)-1:int(len(combinations_list)/2)-1:-1])
    return combinations_list

def gini_index(data):
    count = len(data)
    gini = 1
    feature_values = {}
    for value in data:
        if value not in feature_values.key():
            feature_values[value] = 1
        else:
            feature_values[value] += 1
    for values in feature_values.keys():
        pro = float(feature_values[values]) / count
        gini -= pro^2
    return gini

def split_data(data, column, value):
    left_list = []
    right_list = []
    split_list = []
    for rows in data:
        for values in value:
            if rows[column] == values:
                left_list = data[:column]
                right_list = data[column+1:]
    
    return left_list, right_list

def unique_counts(rows):
    results = {}
    for row in rows:
        r = row[-1]
        if r not in results:
            results[r] = 1
        else:
            results[r] += 1
    return results

def choose_features(data):
    gini_gain = 0
    unique_features = []
    unique = None
    gini_max = 1
    for i in range(len(data[0])):
        unqiue = unique_counts(data[i])
        if unique not in unique_features:
            unique_features.append(unqiue)
        for split in features_com(unique_features):
            if len(split) == 1:
                continue
            left_list, right_list = split_data(data, i, split)
            left_pro = float(len(left_list) / len(data))
            right_pro = float(len(right_list) / len(data))
            gini_gain += left_pro * gini_index(left_list)
            gini_gain += right_pro * gini_index(right_list)
            if gini_gain <= gini_max:
                gini_max = gini_gain
                choose_feature_index = i
                choose_split = left_list, right_list     
    return choose_feature_index, choose_split



def tree(data, ratings):
    choose_feature_index, choose_split = choose_features(data)
    best_feature_rating = ratings[choose_feature_index]
    if choose_feature_index == -1:
        rating_count={}
        for rating in real_rating:
            if rating not in rating_count.keys(): 
                rating_count[rating] = 0
            rating_count[rating] += 1
        sorted_rating_count = sorted(rating_count.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sorted_rating_count[0][0]
    decision_tree = {choose_feature_index:{}}
    best_feature_values = [rows[choose_feature_index] for rows in data]
    best_feature_values = list(set(best_feature_values))
    for value in choose_split:
        if len(value) < 2:
            del(ratings[choose_feature_index])
        decision_tree[best_feature_rating][value] = tree(split_data(data, choose_feature_index, value), ratings)
    return decision_tree

my_tree = tree(train_data[:1516], real_rating)
print(12)
print(my_tree)
print(123)



            



