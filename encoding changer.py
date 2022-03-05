from os import listdir
for filename in listdir("fanfic texts"):
    with open("fanfic texts/" + filename, encoding='windows-1251') as file_in:
        with open("fanfics/" + filename, "w", encoding='utf8') as file_out:
            file_out.write(file_in.read())
