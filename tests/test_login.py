import pytest
from tests.pages.login_page import LoginPage


class TestPositivesScenarios:
    @pytest.mark.login
    def test_positive_login(self, driver, creds):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.execute_login(creds["username"], creds["password"])