import undetected_chromedriver.v2 as uc
linkfan = "https://ficbook.net/readfic/165047"
def get_fanfic(linkfan):
    driver = uc.Chrome()
    with driver:
        # передаём драйверу строку 
        driver.get(linkfan)
    with driver:
        element = driver.find_element(by="id", value="content")
        with open("fanfics/" + linkfan.split("/")[-1] + ".txt", "w") as file:
            file.write(element.get_attribute('innerText'))
    driver.close()
    driver.quit()
with open("in.txt") as file:
    for line in file.readlines():
        get_fanfic(line.strip())
