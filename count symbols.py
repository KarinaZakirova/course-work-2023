from os import listdir
symbols = 0
words = 0
for filename in listdir("fanfics"):
    with open("fanfics/" + filename, "r", encoding='utf8') as file:
        text = file.read()
        symbols += len(text)
        words += len(text.split())
print(symbols)
print(words)
