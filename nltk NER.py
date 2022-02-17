import nltk
from nltk.tokenize import PunktSentenceTokenizer

file_name = 'corpus NER.txt'

def named_entity_recognition(text: str) -> list or str:
    named_entities = []

    # the list of sentences
    tokenized = PunktSentenceTokenizer().tokenize(text)
    
    try:
        for i in tokenized:
            # pipeline
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            tree = nltk.ne_chunk(tagged, binary=True)
            # tree.draw()
            # for each branch in tree-sentence
            for subtree in tree.subtrees():
                if subtree.label() == 'NE':
                    text = str(subtree)
                    # remove markup from named entity 
                    text_clean = ' '.join([word.split('/')[0] for word in text.split() if '(' not in word])
                    named_entities.append(text_clean)
                    print(subtree)

        return named_entities
    
    except Exception as e:
        return str(e)
    
# with open(file_name, encoding='utf-8') as file:
#     print(named_entity_recognition(file.read()))

import os
for filename in os.listdir("fanfics"):
    with open("fanfics/" + filename, encoding='windows-1251') as file:
        print(named_entity_recognition(file.read()))
