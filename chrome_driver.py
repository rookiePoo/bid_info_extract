# -*- coding: UTF-8 -*-

from selenium import webdriver
import time


class ChromeDriver:
    def __init__(self, driver_path, implicit_wait_time=10):
        self.driver = webdriver.Chrome(driver_path)
        self.driver.implicitly_wait(implicit_wait_time)

    def get_response(self, url):
        self.driver.get(url)
        time.sleep(1)