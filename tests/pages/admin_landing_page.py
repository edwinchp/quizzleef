
from .page_page import BasePage
from selenium.webdriver.remote.webdriver import WebDriver

class AdminLandingPage(BasePage):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def get_title(self) -> str:
        return self.title
