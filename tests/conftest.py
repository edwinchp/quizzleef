import hashlib
import os

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

_TESTS_ENV = Path(__file__).resolve().parent / ".env"
if _TESTS_ENV.exists():
    load_dotenv(dotenv_path=_TESTS_ENV, override=False)


@pytest.fixture()
def test_data():
    return {
        "username": os.getenv("TEST_USERNAME", ""),
        "password": os.getenv("TEST_PASSWORD", ""),
        "base_url": os.getenv("TEST_BASE_URL", "http://localhost:8012"),
    }

@pytest.fixture()
def driver(request):
    browser = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")
    print(f"Creating {browser} Driver")
    if browser == "chrome":
        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument("--headless")

        my_driver = webdriver.Chrome(options=chrome_options)

    elif browser == "firefox":
        ff_options = FirefoxOptions()
        if headless:
            ff_options.add_argument("--headless")
        my_driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=ff_options,
        )

    elif browser == 'grid':
        selenium_grid_hub = os.getenv('SELENIUM_GRID_HUB')
        options = FirefoxOptions()
        if headless:
            options.add_argument('--headless')

        my_driver = webdriver.Remote(command_executor=selenium_grid_hub, options=options)
    else:
        raise TypeError(f"Browser not supported: {browser}")
    my_driver.implicitly_wait(30)
    yield my_driver
    print(f"Closing {browser} Driver")
    my_driver.quit()


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser to execute tests (chrome or firefox)"
    )
    parser.addoption(
        "--headless", action="store", default=False, help="Run browser in headless mode"
    )

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            screenshot_dir = "reports/screenshots/"
            os.makedirs(screenshot_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            hash_id = hashlib.md5(item.nodeid.encode()).hexdigest()[:16].replace(" ", "_").replace("/", "_")
            file_name = f"{timestamp}_{hash_id}.png"
            destination = screenshot_dir + file_name
            driver.save_screenshot(destination)

            # Attach to HTML report
            if hasattr(item.config, "_html"):
                extra = getattr(rep, "extra", [])
                html = f'<div><img src="screenshots/{file_name}" alt="screenshot" style="width:400px;" onclick="window.open(this.src)" /></div>'
                extra.append(pytest_html.extras.html(html))
                rep.extra = extra

def pytest_configure(config):
    global pytest_html
    pytest_html = config.pluginmanager.getplugin("html")
    config._html = pytest_html