import pytest
from tests.pages.login_page import LoginPage
from tests.pages.landing_page import LandingPage


class TestPositivesScenarios:
    @pytest.mark.login
    def test_positive_login(self, driver, test_data):

        landing_page = LandingPage(driver)
        landing_page.open()
        landing_page.go_to_administrator_page()
        login_page = LoginPage(driver)
        login_page.execute_login(test_data["username"], test_data["password"])