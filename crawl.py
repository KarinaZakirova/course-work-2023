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

    def __enter__(self):
        """
        Currently, no setup involved.
        """
        logger.debug(f"start chrome")
        self.driver = uc.Chrome()
        logger.debug(f"started chrome")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        When finished or crashed, quit driver.
        """
        self.driver.quit()

    def add_links(self, links):
        # Skip links to fanfics that have already been scraped.
        new_links = [link for link in links if not isfile(get_file_path(link))]
        self.links.extend(new_links)
        logger.debug(f"learned {len(new_links)} links (total: {len(self.links)})")

    def add_text(self, link, text):
        """
        New text has been received. Count the text and save it on the disk.
        """
        with open(get_file_path(link), "w", encoding="utf-8") as f:
            f.write(text)

        logger.debug(f"added text (total: {len(listdir('fanfics/'))})")

    def get_new_seed(self):
        """
        Yields a new link to a search page containing a list of fanfics.
        """
        for page in range(1, 100):
            logger.debug(f"get new seed #{page}")
            yield self.query.format(page)

    def run(self, pagecount=2):
        logger.debug(f"start running")
        while True:
            if not self.links:
                # Ran out of fanfic links.
                # Need to get new ones from Search page.
                self.get_links(next(self.get_new_seed()))
                continue
            link = self.links.pop()
            logger.debug(f"{link}")
            self.get_text_or_links(link)

    def load(self, link):
        if self.driver.current_url == link:
            logger.debug(f"same page, skip reloading - {link}")
            return
        logger.debug(f"loading - {link}")
        with self.driver:
            self.driver.get(link)
        logger.debug(f"loaded - {link}")

    def get_links(self, seed):
        self.load(seed)
        with self.driver:
            # find link tags
            elements = self.driver.find_elements(By.CLASS_NAME, "visit-link")
            # extract links from tags
            links = [i.get_attribute('href') for i in elements]
            links = [link for link in links if link]
        logger.debug(f"found links - {seed}")
        # self.driver.close()
        self.add_links(links)

    def get_text_or_links(self, link):
        self.load(link)
        try:
            with self.driver:
                element = self.driver.find_element(by="id", value="content")
                text = element.get_attribute('innerText')
            # self.driver.close()
            logger.debug(f"found text - {link}")
            self.add_text(link, text)

        except NoSuchElementException:
            # page contains no text
            logger.debug(f"no text, trying links - {link}")
            self.get_links(link)

def get_file_path(link):
    return "fanfics/" + re.sub(r"[^0-9]+", "", link) + ".txt" 



logger = logging.getLogger('crawl')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

if __name__ == "__main__":
    logger.debug(f"start")
    with Crawler() as crawler:
        crawler.run(3)
    # ner_to_csv()
