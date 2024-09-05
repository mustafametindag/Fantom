from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.options import BaseOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver import Chrome, Firefox, Edge


def get_browser_options(browser: str) -> BaseOptions:
    browser_options = {
        "chrome": ChromeOptions,
        "firefox": FirefoxOptions,
        "edge": EdgeOptions,
    }
    return browser_options[browser.lower()]()


def get_manager(browser: str):
    managers = {
        "chrome": ChromeDriverManager,
        "firefox": GeckoDriverManager,
        "edge": EdgeChromiumDriverManager,
    }
    return managers[browser.lower()]()


def get_web_driver(browser: str):
    drivers = {
        "chrome": Chrome,
        "firefox": Firefox,
        "edge": Edge,
    }
    return drivers[browser.lower()]
