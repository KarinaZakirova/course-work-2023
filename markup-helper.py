import os, re

for filename in os.listdir("fanfics/"):
    with open(f"fanfics/{filename}") as f:
        for word in f.read().split():
            if re.match("[А-Я][а-я]*", word):
                print(word)
