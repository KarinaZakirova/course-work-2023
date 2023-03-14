from os import listdir

def diff(
        truth_dir="entities/manual-2/",
        test_dir="entities/ourmodel/",
    ):

    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for filename in listdir(truth_dir):

        # print("===============================")
        # print(filename)

        if not filename in listdir(test_dir):
            continue

        # Load ground truth
        with open(truth_dir + filename, encoding="utf-8") as f:
            truth = set(f.read().split("\n")) - {"", " "}

        # Load test
        with open(test_dir + filename, encoding="utf-8") as f:
            test = set(f.read().split("\n")) - {"", " "}


        true_positives += len(truth & test)
        false_positives += len(test - truth)
        false_negatives += len(truth - test)

        """
        if test & truth:
            print("true positives", test & truth)
        if test - truth:
            print("false positives", test - truth)
        if truth - test:
            print("false negatives", truth - test)
        """

    # print(true_positives, false_positives, false_negatives)
    print("testing", test_dir)
    print("precision:", round(100 * true_positives / (true_positives + false_positives), 2), "%")
    print("recall:", round(100 * true_positives / (true_positives + false_negatives), 2), "%")

if __name__ == "__main__":
    diff()
