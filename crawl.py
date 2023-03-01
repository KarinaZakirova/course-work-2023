import undetected_chromedriver.v2 as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException

from os.path import isfile
from os import listdir
import re

import logging

from threading import Thread


class Crawler:
    def __init__(self, worker_count, text_limit):
        self.workers = [Worker(self, index) for index in range(worker_count)]
        self.logger = new_logger("crawler")
        self.text_limit = text_limit
        self.links = []
        self.tried_links = set()
        self.query = "https://ficbook.net/find?fandom_filter=originals&fandom_group_id=1&pages_range=1&pages_min=&pages_max=&ratings%5B%5D=5&transl=1&tags_include%5B%5D=1669&likes_min=&likes_max=&rewards_min=&date_create_min=2023-02-27&date_create_max=2023-02-27&date_update_min=2023-02-27&date_update_max=2023-02-27&title=&sort=4&rnd=1018693467&find=%D0%9D%D0%B0%D0%B9%D1%82%D0%B8%21&p={}"
        self.query_page = 0

    def get_new_seed(self):
        """
        Yields a new link to a search page containing a list of fanfics.
        """
        self.query_page += 1
        self.logger.debug(f"get new seed #{self.query_page}")
        return self.query.format(self.query_page)

    def run(self):
        self.logger.debug(f"start running")
        for index, worker in enumerate(self.workers):
            Thread(target = self.run_job_queue, args=(worker,), name=f"W_{index}").start()

    def run_job_queue(self, worker):
        worker.start()
        while len(listdir('fanfics/')) < self.text_limit:
            if not self.links:
                # Ran out of fanfic links.
                # Need to get new ones from Search page.
                worker.get_links(self.get_new_seed())
                continue
            worker.get_text_or_links(self.get_link())

    def get_link(self):
        link = self.links.pop()
        self.tried_links.add(link)
        return link


class Worker:
    def __init__(self, crawler, index):
        self.crawler = crawler
        self.driver = None
        self.logger = new_logger(f"worker{index}")

    def start(self):
        self.logger.debug(f"start chrome")
        self.driver = uc.Chrome()
        self.logger.debug(f"started chrome")

    def load(self, link):
        if self.driver.current_url == link:
            self.logger.debug(f"same page, skip reloading - {link}")
            return
        self.logger.debug(f"loading - {link}")
        with self.driver:
            self.driver.get(link)
            # element = WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.TAG_NAME, "article"))
            # )
        self.logger.debug(f"loaded - {link}")

    def add_links(self, links):
        """
        Skip links to fanfics that have already been scraped.
        """
        count = 0
        for link in links:
            if isfile(get_file_path(link)):
                # Already downloaded.
                continue
            if link in self.crawler.links:
                # Already queued.
                continue
            if link in self.crawler.tried_links:
                # Already crawled before.
                # (Might seem irrelevant, but likely helpful for fanfics with pages in them.)
                continue
            self.crawler.links.append(link)
            count += 1
        self.logger.debug(f"learned {count} links (total: {len(self.crawler.links)})")

    def add_text(self, link, text):
        """
        New text has been received. Count the text and save it on the disk.
        """
        with open(get_file_path(link), "w", encoding="utf-8") as f:
            f.write(text)

        self.logger.debug(f"added text (total: {len(listdir('fanfics/'))})")

    def get_links(self, seed):
        self.load(seed)
        with self.driver:
            # find link tags
            elements = self.driver.find_elements(By.CLASS_NAME, "visit-link")
            # extract links from tags
            links = [i.get_attribute('href') for i in elements]
            links = [link for link in links if link]
        self.logger.debug(f"found links - {seed}")
        # self.driver.close()
        self.add_links(links)

    def get_text_or_links(self, link):
        self.load(link)
        try:
            with self.driver:
                element = self.driver.find_element(by="id", value="content")
                text = element.get_attribute('innerText')
            # self.driver.close()
            self.logger.debug(f"found text - {link}")
            self.add_text(link, text)

        except NoSuchElementException:
            # page contains no text
            self.logger.debug(f"no text, trying links - {link}")
            self.get_links(link)

def get_file_path(link):
    return "fanfics/" + re.sub(r"[^0-9]+", "", link) + ".txt" 


def new_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger

if __name__ == "__main__":
    crawler = Crawler(4, 20000)
    crawler.run()
