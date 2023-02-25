import undetected_chromedriver.v2 as uc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from os.path import isfile
from os import listdir
import spacy
import re
from itertools import zip_longest

nlp = spacy.load("ru_core_news_lg")
query = "https://ficbook.net/find?fandom_filter=originals&fandom_group_id=1&pages_range=1&pages_min=&pages_max=&transl=1&likes_min=&likes_max=&rewards_min=&date_create_min=2022-01-05&date_create_max=2022-02-05&date_update_min=2022-01-05&date_update_max=2022-02-05&title=&sort=1&rnd=152877722&find=Найти%21&p={}"


def get_links(seed):
    driver = uc.Chrome()
    with driver:
        # open the page with more links
        driver.get(seed)
    with driver:
        # find link tags
        elements = driver.find_elements(By.CLASS_NAME, "visit-link")
        # extract links from tags
        links = [i.get_attribute('href') for i in elements]
        links = [link for link in links if link]
    driver.close()
    driver.quit()
    return links


def get_file_path(link):
    return "fanfics/" + re.sub(r"[^0-9]+", "", link) + ".txt" 


def get_text_or_links(link):
    driver = uc.Chrome()
    if isfile(get_file_path(link)):
        return
    with driver:
        # open the page with text
        driver.get(link)
    try:
        with driver:
            element = driver.find_element(by="id", value="content")
            text = element.get_attribute('innerText')
        driver.close()
        driver.quit()
        return text
    except NoSuchElementException:
        # page contains no text
        print(link, "no text found. attempting links")
        return get_links(link)


def scrape_for_fanfics(pagecount=2):
    # collect links to fanfics
    links = []
    seeds = [query.format(page) for page in range(1, pagecount)]
    for seed in seeds:
        links.extend(get_links(seed))
    while links:
        link = links.pop()
        print(link)
        text = get_text_or_links(link)
        if isinstance(text, list):
            links.extend(text)
        elif text:
            with open(get_file_path(link), "w", encoding="utf8") as file:
                file.write(text)

if __name__ == "__main__":
    scrape_for_fanfics(2)
    # ner_to_csv()