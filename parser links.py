import undetected_chromedriver.v2 as uc
linkfan = "https://ficbook.net/find?fandom_filter=originals&fandom_group_id=1&pages_range=1&pages_min=&pages_max=&transl=1&likes_min=&likes_max=&rewards_min=&date_create_min=2022-01-05&date_create_max=2022-02-05&date_update_min=2022-01-05&date_update_max=2022-02-05&title=&sort=1&rnd=152877722&find=Найти%21&p={}"
def get_fanfic(linkfan):
    driver = uc.Chrome()
    with driver:
        # передаём драйверу строку 
        driver.get(linkfan)
    with driver:
        elements = driver.find_elements_by_class_name("visit-link")
        with open("links.txt", "w") as file:
            for element in elements:
                file.write(element.get_attribute('href'))
        # with open("fanfics/" + linkfan.split("/")[-1] + ".txt", "w") as file:
            # file.write(element.get_attribute('innerText'))
    driver.close()
    driver.quit()
for i in range(1, 10):
    get_fanfic(linkfan.format(i))
