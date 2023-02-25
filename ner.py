import undetected_chromedriver.v2 as uc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from os.path import isfile
from os import listdir
import spacy
import re
from itertools import zip_longest

nlp = spacy.load("ru_core_news_lg")

def named_entity_recognition(a):
    doc = nlp(a)
    named_entities = []
    for ent in doc.ents:
        if ent.label_ == "PER":
            named_entities.append(ent.text.replace('\n', " "))
    return named_entities

def frequency(iterable):
    occurences = {}
    for i in iterable:
        if i not in occurences:
            occurences[i] = 0
        occurences[i] += 1
    return sorted(occurences.items(), key=lambda x: x[1], reverse=True)


def show_ner():
    named_entities = []
    for filename in listdir("fanfics"):
        with open("fanfics/" + filename, encoding='utf8') as file:
            named_entities.extend(named_entity_recognition(file.read()))
    for key, value in frequency(named_entities):
        print(f"{key}\t{value}")


def ner_to_csv():
    named_entities = []
    for filename in listdir("fanfics"):
        with open("fanfics/" + filename, encoding='utf8') as file:
            print("NLP:", filename)
            named_entities.append([filename])
            named_entities[-1].extend(named_entity_recognition(file.read()))
    with open("out.csv", "w", encoding="utf8") as file:
        for row in zip_longest(*named_entities, fillvalue=""):
            print(",".join(row) + "\n")
            file.write(",".join(row) + "\n")

if __name__ == "__main__":
    ner_to_csv()
