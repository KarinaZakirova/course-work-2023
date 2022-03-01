def get_fanfic(linkfan):
    driver = uc.Chrome()
    with driver:
        # передаём драйверу строку 
        driver.get(linkfan)
    with driver:
        elements = driver.find_elements_by_class_name("visit-link")
        with open("links.txt", "w") as file:
            for element in elements:
                file.write(element.get_attribute('href') + "\n") 
        # with open("fanfics/" + linkfan.split("/")[-1] + ".txt", "w") as file:
            # file.write(element.get_attribute('innerText'))
    driver.close()
    driver.quit()

def get_fanfic(linkfan):
    filepath = "fanfics/" + linkfan.split("/")[-1] + ".txt"
    if isfile(filepath):
        return
    driver = uc.Chrome()
    with driver:
        # передаём драйверу строку 
        driver.get(linkfan)
    try:
        with driver:
            element = driver.find_element(by="id", value="content")
            with open(filepath, "w") as file:
                file.write(element.get_attribute('innerText'))
        driver.close()
        driver.quit()
    except NoSuchElementException:
        print(linkfan, "none")

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

    
