from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from .page_page import BasePage


class LoginPage(BasePage):
    __username_field = (By.NAME, "username")
    __password_field = (By.NAME, "password")
    __submit_button = (By.XPATH, "//input[@type='submit']")
    __error_message = (By.ID, "error")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def open(self, url: str):
        super()._open(url + '/admin/login/')

    def execute_login(self, username : str, password : str):
        super()._type(self.__username_field, username)
        super()._type(self.__password_field, password)
        super()._click(self.__submit_button)

    @property
    def error_message(self) -> str:
        return super()._get_text(self.__error_message)

    @property
    def current_url(self) -> str:
        return super().current_url