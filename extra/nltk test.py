import nltk
sentence = 'This is a sentence.'
tokens = nltk.word_tokenize(sentence)
tagged_tokens = nltk.pos_tag(tokens)
print(tagged_tokens)
tokens = nltk.word_tokenize('I am very excited about the next generation of Apple products.')
tokens = nltk.pos_tag(tokens)
tree = nltk.ne_chunk(tokens)
print(tree)
