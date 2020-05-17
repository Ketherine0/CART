from classification import *
if __name__ == "__main__":
    # get data
    train_data = openFile("train.csv")
    test_data = openFile("test.csv")
    # train and pruning
    total_len = len(train_data[:6072])
    my_tree = createTree(train_data[:6072],total_len)
    accuracy = finalTest(test_data, my_tree)
    print("The original final accuracy is :", accuracy)
    tree_list = pruning(my_tree)
    print("They are trees:", tree_list)
    best_tree, best_accuracy, accuracy_list = validation(train_data[6072:], tree_list)
    print("The best tree:", best_tree, best_accuracy)
    print(accuracy_list)
    # test
    accuracy = finalTest(test_data, best_tree)
    print("The final accuracy is :", accuracy)