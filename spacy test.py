import spacy 
nlp = spacy.load("ru_core_news_sm")
a = """
20 декабря Дмитрий Анатольевич посетил Саяно-Шушенскую ГЭС и поговорил с её начальством."""

def named_entity_recognition(a):
    doc = nlp(a)
    named_entities = []
    for ent in doc.ents:
        named_entities.append(ent.text,
              # ent.label_
              )        
    return named_entities
    # ner_list = nlp.pipe_labels['ner']
    # for ner_category in ner_list:
        # print("{} ({})".format(ner_category, spacy.explain(ner_category)))

import os
named_entities = []
for filename in os.listdir("fanfics"):
    with open("fanfics/" + filename, encoding='windows-1251') as file:
        named_entities.extend(named_entity_recognition(file.read()))
        
occurences = {}
for i in named_entities:
    if i not in occurences:
        occurences[i] = 0
    occurences[i] += 1
for key, value in sorted(occurences.items(), key=lambda x: x[1], reverse=True):
    print(key, value)


