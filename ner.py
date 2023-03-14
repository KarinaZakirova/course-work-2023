import undetected_chromedriver.v2 as uc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from os.path import isfile
from os import listdir
import spacy
import re
from itertools import zip_longest, groupby
from pymystem3 import Mystem
from collections import Counter
import csv

nlp = spacy.load("ru_core_news_sm")
# nlp = spacy.load("ru_core_news_lg")
# nlp = spacy.load("training/output/model-last")


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


def extract_entities(
        in_dir="fanfics/",
        out_dir="entities/",
    ):
    for index, filename in enumerate(listdir(in_dir)):
        print(index, "extracting entities:", filename)

        if filename in listdir(out_dir):
            continue

        # Read fanfic, extract named entities
        with open(in_dir + filename, encoding='utf8') as f:
            text = f.read()
            named_entities = sorted(set(named_entity_recognition(text)), key=len, reverse=True)

        # Save entities
        with open(out_dir + filename, "w", encoding="utf-8") as f:
            f.write("\n".join(named_entities))

def corpus_markup(
        text_dir="fanfics/",
        entity_dir="entities/",
        out_dir="ner/",
    ):
    for index, filename in enumerate(listdir(entity_dir)):
        print(index, "adding markup:", filename)

        if filename in listdir(out_dir):
            continue

        # Read fanfic
        with open(text_dir + filename, encoding='utf8') as f:
            text = f.read()

        # Load entities
        with open(entity_dir + filename, encoding="utf-8") as f:
            named_entities = f.read().split("\n")

        # Use entities to add markup
        with open(out_dir + filename, "w", encoding="utf-8") as f:
            for entity in named_entities:
                # Add brackets around every entity.
                # Ordered in the correct way to avoid doubling up or incomplete selections
                text = re.sub(f"(?<!<)({re.escape(entity)}[а-я]*)", r"<\g<1>>", text)
                # Remove bizarre empty marking. I don't know how and why it exists
                text = text.replace("<>", "")
            f.write(text)

    # with open("out.txt", "w", encoding="utf8") as file:
    #     for row in zip_longest(*named_entities, fillvalue=""):
    #         print(",".join(row) + "\n")
    #         file.write(",".join(row) + "\n")

def corpus_reformat(
        text_dir="fanfics/",
        entity_dir="entities-manual/",
    ):
    sentences = []
    for index, filename in enumerate(listdir(entity_dir)):
        # print(index, "reading:", filename)

        # Read fanfic as sentences
        with open(text_dir + filename, encoding='utf8') as f:
            text = re.split('\.|!|\?', f.read())

        # Load entities
        with open(entity_dir + filename, encoding="utf-8") as f:
            named_entities = f.read().split("\n")


        for sentence in text:
            clean_sentence = sentence
            entities = []

            ranges = set()

            for entity in named_entities:
            # tags = [tag for tag in re.findall("\<(.*?)\>", sentence) if tag]
                for match in re.finditer(entity, sentence):
                    new_ranges = set(range(*match.span()))
                    if new_ranges & ranges:
                        # oh no we intersect
                        continue
                    # oh cool we don't
                    ranges.update(new_ranges)
                    entities.append((*match.span(), "PER"))
            if entities:
                sentences.append((sentence, {"entities": entities}))
    return sentences

def knowledge_graph(
        text_dir="ner/",
        entity_dir="entities/",
        out_dir="graph/",
    ):
    mystem = Mystem()
    for key, group in groupby(listdir(entity_dir), lambda x: x[:7]):
        group = list(group)
        # if len(group) > 1:
        #     print(key, len(list(group)))
        print("===============================")
        print(key)

        if key in listdir(out_dir):
            continue

        multipage_tags = []
        for filename in group:
            # print("===============================")
            # print(key, filename)
            with open(text_dir + filename, "r", encoding="utf-8") as f:
                text = re.split('\.|!|\?', f.read())
                for sentence in text:
                    lemmatised = "".join(mystem.lemmatize(sentence))


                    tags = [tag for tag in re.findall("\<(.*?)\>", lemmatised) if tag]
                    if tags:
                        if len("".join(tags))/len(sentence) > 0.5 and len(sentence.split()) > 10:
                            # These are sentences which erroneously received
                            # an unusually high number of tags. Skip them.
                            continue

                        # print(tags)
                        multipage_tags.extend(tags)
        counted_tags = Counter(multipage_tags)
        # for tag in sorted(counted_tags, key=counted_tags.get, reverse=True):
        #     count = counted_tags[tag]
        #     if count > 2:
        #         print(tag, count)
        counted_tags = {k: v for k, v in counted_tags.items() if v > 2}

        tag_groups = []
        for filename in group:
            with open(text_dir + filename, "r", encoding="utf-8") as f:
                text = re.split('\.|!|\?', f.read())
                for sentence in text:
                    lemmatised = "".join(mystem.lemmatize(sentence))
                    tags = [tag for tag in re.findall("\<(.*?)\>", lemmatised) if tag]
                    relevant_tags = set(counted_tags) & set(tags)
                    if len(relevant_tags) > 1:
                        # print(relevant_tags)
                        tag_groups.append(tuple(relevant_tags))

        counted_tag_groups = Counter(tag_groups)
        with open(out_dir + key, "w", encoding="utf-8") as f:
            write = csv.writer(f, dialect='unix')
            for index, tag in enumerate(sorted(counted_tag_groups, key=counted_tag_groups.get, reverse=True)):
                count = counted_tag_groups[tag]
                if len(tag) != 2:
                    # Sentence has multiple tags. Difficult to treat.
                    continue
                if index/len(counted_tag_groups) <= 0.1 and count >= 5:
                    status = "взаимосвязан с"
                elif count >= 2:
                    status = "имеет отношение к"
                else:
                    status = "незначимо связан с"
                write.writerow([tag[0], status, tag[1]])


def clean_entities(
        in_dir="entities/",
        out_dir="clean-entities/",
    ):
    mystem = Mystem()
    for index, filename in enumerate(listdir(in_dir)):

        clean_entities = []
        # dirty_entities = []

        print(index, "cleaning entities:", filename)

        if filename in listdir(out_dir):
            continue

        # Load entities
        with open(in_dir + filename, encoding="utf-8") as f:
            named_entities = f.read().split("\n")

        with open("russian.txt", encoding="utf-8") as f:
            russian = {word for word in f.read().split("\n") if word and word[0].lower() == word[0]}

        for entity in named_entities:
            if not entity:
                continue
            lemma = " ".join(mystem.lemmatize(entity))
            if entity.lower() not in russian:
                clean_entities.append(entity)
            # else:
            #     dirty_entities.append(entity)

        # Save entities
        with open(out_dir + filename, "w", encoding="utf-8") as f:
            # f.write("\n".join(clean_entities) + "\n\n" + "\n".join(dirty_entities))
            f.write("\n".join(clean_entities))


if __name__ == "__main__":
    # extract_entities(out_dir="entities/sm/")
    # corpus_markup()
    # knowledge_graph()
    # clean_entities()
    # corpus_markup(text_dir="fanfics/", entity_dir="entities-manual/", out_dir="ner-manual/")
    # corpus_reformat()
    #extract_entities(out_dir="entities-trained/")
    #corpus_markup(entity_dir="entities-trained/")
    clean_entities(in_dir="entities/ourmodel/", out_dir="entities/ourmodel-clean/")
