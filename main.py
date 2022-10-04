from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time 
from utils import *

class WebDriver():
    def __init__(self):
        DRIVER_PATH = "/Users/ArnoldYanga/Desktop/Selenium/chromedriver"
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    
    def __call__(self, url):
        self.driver.get(url)


if __name__ == '__main__':

    URL = "http://www.ufcstats.com/statistics/events/completed?page=all"

    web_driver = WebDriver()
    web_driver(URL)
    ufc_driver = web_driver.driver

    links = ufc_driver.find_elements(By.XPATH, "//tr[@class='b-statistics__table-row']//td//i//a")
    j = -1

    for i in range(len(links)):
        event = ufc_driver.find_elements(By.XPATH, "//tr[@class='b-statistics__table-row']//td//i//a")[j]
        event.click()

        time.sleep(4)
        fight_element_xpath = "//tr[@class='b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click']"
        fights = ufc_driver.find_elements(By.XPATH, fight_element_xpath)

        j -= 1

        for fight in fights:
            fight.click()
            data = {}

            data = collect_fight_info(ufc_driver, data)

            try:
                data = {**data, **collect_fight_stats(ufc_driver)}
            except:
                pass
            
            print(data)
            ufc_driver.back()

        ufc_driver.back()

