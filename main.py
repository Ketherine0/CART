from src import openFile, createTree, final_test, pruning, validation

if __name__ == "__main__":
    rows = openFile('test.csv')
    datasets = openFile('test.csv')

    total_len = len(rows)
    my_tree = createTree(rows)
    accuracy = final_test(datasets, my_tree)
    print("The original final accuracy is :", accuracy)

    tree_list = pruning(my_tree)
    best_tree, best_accuracy, accuracy_list = validation(rows[6072:], tree_list)
    accuracy = final_test(datasets, best_tree)
    print("The final accuracy is :", accuracy)