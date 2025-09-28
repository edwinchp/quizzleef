from selenium.webdriver.common.by import By
from .page_page import BasePage 
from selenium.webdriver.remote.webdriver import WebDriver
import os
from typing import Optional


class LandingPage(BasePage):
    __administrator_link = (By.LINK_TEXT, "Administrator")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def open(self, url: Optional[str] = None):
        if not url:
            url = os.getenv("TEST_BASE_URL", "http://localhost:8012")
        super()._open(url)

    def go_to_administrator_page(self):
        super()._click(self.__administrator_link)