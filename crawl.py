import undetected_chromedriver.v2 as uc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from os.path import isfile
from os import listdir
import spacy
import re
from itertools import zip_longest

import logging

query = "https://ficbook.net/find?fandom_filter=originals&fandom_group_id=1&pages_range=1&pages_min=&pages_max=&ratings%5B%5D=5&ratings%5B%5D=6&transl=1&likes_min=&likes_max=&rewards_min=&date_create_min=2023-02-25&date_create_max=2023-02-25&date_update_min=2023-02-25&date_update_max=2023-02-25&title=&sort=1&rnd=679840539&find=%D0%9D%D0%B0%D0%B9%D1%82%D0%B8%21&p={}"


def get_links(seed):
    logger.debug(f"starting chrome for\t{seed}")
    driver = uc.Chrome()
    logger.debug(f"started chrome for\t{seed}")
    with driver:
        # open the page with more links
        driver.get(seed)
    logger.debug(f"opened page for\t{seed}")
    with driver:
        # find link tags
        elements = driver.find_elements(By.CLASS_NAME, "visit-link")
        # extract links from tags
        links = [i.get_attribute('href') for i in elements]
        links = [link for link in links if link]
    logger.debug(f"found elements for\t{seed}")
    driver.close()
    driver.quit()
    return links


def get_file_path(link):
    return "fanfics/" + re.sub(r"[^0-9]+", "", link) + ".txt" 


def get_text_or_links(link):
    logger.debug(f"starting chrome for\t{link}")
    driver = uc.Chrome()
    logger.debug(f"started chrome for\t{link}")
    if isfile(get_file_path(link)):
        return
    with driver:
        # open the page with text
        driver.get(link)
    logger.debug(f"opened page for\t{link}")
    try:
        with driver:
            element = driver.find_element(by="id", value="content")
            text = element.get_attribute('innerText')
        driver.close()
        driver.quit()
        logger.debug(f"found text, quit for\t{link}")
        return text
    except NoSuchElementException:
        # page contains no text
        logger.debug(f"no text found, links for \t{link}")
        return get_links(link)


def scrape_for_fanfics(pagecount=2):
    # collect links to fanfics
    links = []
    seeds = [query.format(page) for page in range(1, pagecount)]
    for seed in seeds:
        links.extend(get_links(seed))
    while links:
        link = links.pop()
        logger.debug(f"{link}")
        text = get_text_or_links(link)
        if isinstance(text, list):
            links.extend(text)
        elif text:
            with open(get_file_path(link), "w", encoding="utf8") as file:
                file.write(text)


logger = logging.getLogger('crawl')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

if __name__ == "__main__":
    scrape_for_fanfics(20)
    logger.debug(f"start")
    # ner_to_csv()
