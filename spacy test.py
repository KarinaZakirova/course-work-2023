import spacy 
nlp = spacy.load("ru_core_news_sm")
a = """
20 декабря Дмитрий Анатольевич посетил Саяно-Шушенскую ГЭС и поговорил с её начальством."""
doc = nlp(a)
for ent in doc.ents:
    print(ent.text,  ent.label_)

ner_list = nlp.pipe_labels['ner']
for ner_category in ner_list:
    print("{} ({})".format(ner_category, spacy.explain(ner_category)))
