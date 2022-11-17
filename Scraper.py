from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper():

    selector_types = {"id": By.ID, "class_name": By.CLASS_NAME,
                      "tag": By.TAG_NAME, "xpath": By.XPATH, "css_selector": By.CSS_SELECTOR}

    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("start-fullscreen")
    options.add_argument("--log-level=3")
    # options.add_argument("user-data-dir=selenium")

    def __init__(self, initial_link):
        self.initial_link = initial_link
        self.driver = webdriver.Chrome(
            executable_path="./chromedriver.exe", options=self.options)
        self.driver.get(initial_link)

        self.tabs = []
        self.current_tab_index = 0

    # get all elements by id, class, tag or xpath

    def get_all(self, selector_type, selector):

        elements = self.driver.find_elements(
            self.selector_types[selector_type], selector)
        return elements

    # gets all elements by id, class, tag or xpath and prints their text

    def print_all_text(self, selector_type, selector):

        for element in self.get_all(selector_type, selector):
            print(element.text)
            print()
    # scrape from children only

    def get_children(self, parent, selector_type, selector):
        children = parent.find_elements(
            self.selector_types[selector_type], selector)
        return children

    # scrape a lazy load site
    def get_lazy(self, selector_type="", selector="", max=100, func=False):

        elements = []

        while len(elements) < max:
            print(f"Got {str(len(elements))}")
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            if (func == False):
                temp_elements = self.get_all(selector_type, selector)
            else:
                temp_elements = func()

            num_of_elements = len(temp_elements)
            if (num_of_elements > len(elements)):
                elements = temp_elements

            else:
                time.sleep(1)

            self.driver.execute_script(
                "window.scrollTo(0,0);")

        return elements

    def dump_csv(self, file, header, data):
        with open(file+".csv", 'w', encoding='UTF-8', newline='') as f:
            writer = csv.DictWriter(
                f, header)
            writer.writeheader()
            writer.writerows(data)

    def scroll_to(self, element):

        l = element.rect
        script = f"window.scrollTo({l['x']},{l['y']})"
        self.driver.execute_script(f"window.scrollTo({l['x']},{l['y']})")
