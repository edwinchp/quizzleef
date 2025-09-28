import pytest
from tests.pages.login_page import LoginPage


class TestPositivesScenarios:
    @pytest.mark.login
    def test_positive_login(self, driver, test_data):
        login_page = LoginPage(driver)
        login_page.open(test_data["base_url"])
        login_page.execute_login(test_data["username"], test_data["password"])