import undetected_chromedriver.v2 as uc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from os.path import isfile
from os import listdir
import spacy
import re
from itertools import zip_longest

import logging


class Crawler:
    def __init__(self):
        self.driver = None
        self.query = "https://ficbook.net/find?fandom_filter=originals&fandom_group_id=1&pages_range=1&pages_min=&pages_max=&ratings%5B%5D=5&ratings%5B%5D=6&transl=1&likes_min=&likes_max=&rewards_min=&date_create_min=2023-02-25&date_create_max=2023-02-25&date_update_min=2023-02-25&date_update_max=2023-02-25&title=&sort=1&rnd=679840539&find=%D0%9D%D0%B0%D0%B9%D1%82%D0%B8%21&p={}"
        self.links = []
        self.texts = []

    def __enter__(self):
        """
        Currently, no setup involved.
        """
        logger.debug(f"start chrome")
        self.driver = uc.Chrome()
        logger.debug(f"started chrome")
        self.driver.get("https://www.google.com")
        logger.debug(f"opened dummy page")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        When finished or crashed, quit driver.
        """
        self.driver.quit()
        print(len(self.links))
        print(len(self.texts))

    def get_seeds(self, count):
        """
        Turn the query template into several search page links,
        which contain links to fanfics.
        """
        return [self.query.format(page) for page in range(1, count)]

    def run(self, pagecount=2):
        logger.debug(f"started running")
        for seed in self.get_seeds(pagecount):
            self.links.extend(self.get_links(seed))
        logger.debug(f"links: {len(self.links)}")
        while self.links:
            link = self.links.pop()
            logger.debug(f"{link}")
            text = self.get_text_or_links(link)
            if isinstance(text, list):
                self.links.extend(text)
            elif text:
                with open(get_file_path(link), "w", encoding="utf8") as file:
                    file.write(text)

    def get_links(self, seed):
        logger.debug(f"opening page for\t{seed}")
        with self.driver:
            # open the page with more links
            self.driver.get(seed)
        logger.debug(f"opened page for\t{seed}")
        with self.driver:
            # find link tags
            elements = self.driver.find_elements(By.CLASS_NAME, "visit-link")
            # extract links from tags
            links = [i.get_attribute('href') for i in elements]
            links = [link for link in links if link]
        logger.debug(f"found elements for\t{seed}")
        # self.driver.close()
        return links

    def get_text_or_links(self, link):
        logger.debug(f"started chrome for\t{link}")
        if isfile(get_file_path(link)):
            return
        with self.driver:
            # open the page with text
            self.driver.get(link)
        logger.debug(f"opened page for\t{link}")
        try:
            with self.driver:
                element = self.driver.find_element(by="id", value="content")
                text = element.get_attribute('innerText')
            # self.driver.close()
            logger.debug(f"found text, quit for\t{link}")
            return text
        except NoSuchElementException:
            # page contains no text
            logger.debug(f"no text found, links for \t{link}")
            return self.get_links(link)

def get_file_path(link):
    return "fanfics/" + re.sub(r"[^0-9]+", "", link) + ".txt" 



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
    logger.debug(f"start")
    with Crawler() as crawler:
        crawler.run(2)
    # ner_to_csv()
