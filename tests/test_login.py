import pytest
from tests.pages.login_page import LoginPage
from tests.pages.landing_page import LandingPage
from tests.pages.admin_landing_page import AdminLandingPage

class TestPositivesScenarios:
    @pytest.mark.login
    @pytest.mark.parametrize("username, password, expected_title", [
        ("admin", "admin", "Site administration | Django site admin"),
        ("admin", "admin", "Error: Log in | Django site admin"),
    ])
    def test_positive_login(self, driver, test_data):
        landing_page = LandingPage(driver)
        landing_page.open()
        landing_page.go_to_administrator_page()
        login_page = LoginPage(driver)
        login_page.execute_login(test_data["username"], test_data["password"])
        admin_landing_page = AdminLandingPage(driver)
        assert admin_landing_page.title == test_data["expected_title"]