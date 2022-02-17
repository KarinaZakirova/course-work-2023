import undetected_chromedriver.v2 as uc
from selenium.common.exceptions import NoSuchElementException
from os.path import isfile
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
with open("links.txt") as file:
    for line in file.readlines():
        get_fanfic(line.strip()) 

 

 





