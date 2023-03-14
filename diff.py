from os import listdir
import re

def diff(
        truth_dir="entities/manual/",
        test_dir="entities/ourmodel-clean/",
        text_dir="fanfics/",
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

        # Load text
        with open(text_dir + filename, encoding="utf-8") as f:
            text = f.read()

        tp = sum(len(re.findall(re.escape(entity), text)) for entity in truth & test)
        fp = sum(len(re.findall(re.escape(entity), text)) for entity in test - truth)
        fn = sum(len(re.findall(re.escape(entity), text)) for entity in truth - test)
        true_positives += tp
        false_positives += fp
        false_negatives += fn
        # print(entity, tp, fp, fn)

        """
        if test & truth:
            print("true positives", test & truth)
        if test - truth:
            print("false positives", test - truth)
        if truth - test:
            print("false negatives", truth - test)
        """

    print("testing", test_dir)
    print("true positives:", true_positives)
    print("false positives:", false_positives)
    print("false negatives:", false_negatives)
    print("precision:", round(100 * true_positives / (true_positives + false_positives), 2), "%")
    print("recall:", round(100 * true_positives / (true_positives + false_negatives), 2), "%")


def diff_all(
        truth_dir="entities/manual/",
    ):
    for folder in listdir("entities/"):
        test_dir = f"entities/{folder}/"
        if not test_dir == truth_dir:
            print("===========================")
            diff(truth_dir, test_dir)

if __name__ == "__main__":
    diff_all()
