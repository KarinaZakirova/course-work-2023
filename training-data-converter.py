
from ner import corpus_reformat

TRAIN_DATA = corpus_reformat()

# exit()

import pandas as pd
import os
from tqdm import tqdm
import spacy
from spacy.tokens import DocBin

#nlp = spacy.blank("en") # load a new spacy model
nlp = spacy.load("ru_core_news_lg") # load other spacy model

db = DocBin() # create a DocBin object

for text, annot in tqdm(TRAIN_DATA): # data in previous format
    doc = nlp.make_doc(text) # create doc object from text
    ents = []
    for start, end, label in annot["entities"]: # add character indexes
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is None:
            print("Skipping entity")
        else:
            ents.append(span)
    doc.ents = ents # label the text with the ents
    db.add(doc)

# os.chdir(r'XXXX\XXXXX')
db.to_disk("training/train.spacy") # save the docbin object
