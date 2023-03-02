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
            # named_entities.append(ent.lemma_.replace('\n', " "))
            named_entities.append(ent.text.replace('\n', " "))
    return named_entities

    # for token in doc:
    #     if token in doc.ents:
    #         print(token)

    # for ent in doc.ents:
    #     if ent.label_ == "PER":
    #         named_entities.append("<" + ent.text.replace('\n', ' ') + ">")
    #     else:
    #         named_entities.append(ent.text.replace('\n', " "))
    # return " ".join(named_entities)


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


def extract_entities():
    for index, filename in enumerate(listdir("fanfics/")):
        print(index, "extracting entities:", filename)

        if filename in listdir("entities/"):
            continue

        # Read fanfic, extract named entities
        with open("fanfics/" + filename, encoding='utf8') as f:
            text = f.read()
            named_entities = sorted(set(named_entity_recognition(text)), key=len, reverse=True)

        # Save entities
        with open("entities/" + filename, "w", encoding="utf-8") as f:
            f.write("\n".join(named_entities))

def corpus_markup():
    for index, filename in enumerate(listdir("entities/")):
        print(index, "adding markup:", filename)

        if filename in listdir("ner/"):
            continue

        # Read fanfic
        with open("fanfics/" + filename, encoding='utf8') as f:
            text = f.read()

        # Load entities
        with open("entities/" + filename, encoding="utf-8") as f:
            named_entities = f.read().split("\n")

        # Use entities to add markup
        with open("ner/" + filename, "w", encoding="utf-8") as f:
            for entity in named_entities:
                # Add brackets around every entity.
                # Ordered in the correct way to avoid doubling up or incomplete selections
                text = re.sub(f"(?<!<)({re.escape(entity)}[а-я]*)", r"<\g<1>>", text)
            f.write(text)

    # with open("out.txt", "w", encoding="utf8") as file:
    #     for row in zip_longest(*named_entities, fillvalue=""):
    #         print(",".join(row) + "\n")
    #         file.write(",".join(row) + "\n")

if __name__ == "__main__":
    # extract_entities()
    corpus_markup()
