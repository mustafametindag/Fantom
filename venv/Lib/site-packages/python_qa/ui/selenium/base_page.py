import time
import typing
from typing import List

from selenium import webdriver
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import expected_conditions as EC_INT
from . import BaseElement, BaseChildElement
from ...logging.logging import Logging
logger = Logging.logger


class BasePage:

    def __init__(self, driver: webdriver.Remote, host: str = None):
        self.driver = self.d = driver
        self.host = host

    def _wait_page_loaded(self, wait_time: int = 10, wait_step: float = 0.2):
        end_time = time.time() + wait_time
        while time.time() < end_time:
            state = self.d.execute_script("return document.readyState")
            if state == "complete":
                return
            logger.info(f"The page is in '{state}' state. Waiting for the page to load ...")
            time.sleep(wait_step)

    def open(self, url: str = "/"):
        logger.info(f"Opening the page {url}")
        self.d.get(self.host + url)
        self._wait_page_loaded()

    def clear_all_cookies(self):
        logger.info("Clear all Cookies")
        self.driver.execute(
            "SEND_DTP", dict(cmd="Network.clearBrowserCookies", params={})
        )

    def find(self, element, wait_time=5) -> WebElement:
        logger.info(f"Find element {element}")
        return WebDriverWait(self.d, wait_time).until(
            EC.presence_of_element_located(element)
        )

    def finds(self, element, text=None, wait_time=5) -> List[WebElement]:
        logger.info(f"Find element {element}")
        elements = WebDriverWait(self.d, wait_time).until(
            EC.presence_of_all_elements_located(element)
        )
        if text is not None:
            return [el for el in elements if text in el.text]
        else:
            return elements

    def wait_for(
        self, expected_condition, element, wait_time=2, until=True, **kwargs
    ):
        logger.info(f"Wait state {expected_condition} for element {element}")
        driver = self.d
        if isinstance(element, BaseElement):
            element = element.selector
        elif isinstance(element, BaseChildElement):
            element.parent.instance = self
            driver = element.parent()
            element = element.selector
        if until:
            return WebDriverWait(driver, wait_time).until(
                expected_condition(element, **kwargs)
            )
        else:
            return WebDriverWait(driver, wait_time).until_not(
                expected_condition(element, **kwargs)
            )

    def safe_wait_for(
        self,
        expected_condition,
        element,
        error_value: typing.Any = False,
        **kwargs,
    ):
        try:
            return self.wait_for(expected_condition, element, **kwargs)
        except TimeoutException:
            return error_value

    def wait_not_exist(self, element, wait_time=5) -> WebElement:
        logger.info(f"Waiting for the {element} to disappear")
        return self.wait_for(
            EC.presence_of_element_located, element, wait_time, until=False
        )

    def wait_text_appear(self, element, text, wait_time=5) -> WebElement:
        logger.info(f"Waiting for the {text} text to appear in the {element} element")
        return self.wait_for(
            EC.text_to_be_present_in_element, element, wait_time, text_=text
        )

    def wait_clickable(self, element, wait_time=5) -> WebElement:
        return self.wait_for(
            EC_INT.presence_element_to_be_clickable, element, wait_time
        )

    def wait_visible(self, element, wait_time=5) -> WebElement:
        return self.wait_for(
            EC.visibility_of_element_located, element, wait_time
        )

    def wait_visible_all(self, element, wait_time=5) -> WebElement:
        return self.wait_for(
            EC.visibility_of_all_elements_located, element, wait_time
        )

    def wait_not_visible(self, element, wait_time=5) -> WebElement:
        return self.wait_for(
            EC.invisibility_of_element_located, element, wait_time
        )

    def wait_presence_all(self, element, wait_time=5) -> List[WebElement]:
        return self.wait_for(
            EC.presence_of_all_elements_located, element, wait_time
        )

    def wait_element_with_text_appear(
        self, element, text, wait_time=5
    ) -> WebElement:
        return self.wait_for(
            EC_INT.element_located_with_text, element, wait_time, text=text
        )

    def wait_text_in_element(self, element, text, wait_time=5) -> WebElement:
        return self.wait_for(
            EC_INT.element_with_text, element, wait_time, text=text
        )

    def wait_staleness_of(self, element, wait_time=5):
        return self.safe_wait_for(
            EC.staleness_of, element, wait_time, until=True
        )

    def wait_animation_end(
        self,
        element: typing.Union[BaseElement, BaseChildElement, WebElement],
        wait_time=5,
    ):
        script = """
        elem = arguments[0];
        elem.addEventListener("transitionend", function(event) {
          elem.setAttribute('data-animating', false);
        }, false);
        """
        if isinstance(element, WebElement):
            self.d.execute_script(script, element)
        else:
            self.d.execute_script(script, element())
        return self.wait_for(EC_INT.animation_ended, element, wait_time)

    def wait_number_of_all_elements(
        self, element, number, wait_time=5
    ) -> WebElement:
        return self.safe_wait_for(
            EC_INT.number_of_all_elements_located,
            element,
            error_value=[],
            wait_time=wait_time,
            number=number,
        )

    def find_pseudo_attribute(self, element, attribute):
        query_selector = (
            "return window.getComputedStyle("
            "arguments[0],':{0}'"
            ").getPropertyValue('content')".format(attribute)
        )
        return self.d.execute_script(query_selector, element)

    f = find
    fpa = find_pseudo_attribute

    def get_page_title(self):
        logger.info(f"Check page title {self.d.title}")
        return self.d.title

    def get_url(self):
        logger.info(f"Check url page {self.d.current_url}")
        return self.d.current_url

    def wait_url(self, url, wait_time=3):
        return WebDriverWait(self.d, wait_time).until(EC.url_matches(url))

    def select(self, select_selector, _id=None, name=None,):
        if (not _id and not name) or (_id and name):
            raise ValueError("You should provide either _id or name")
        self.wait_visible(select_selector)
        options = self.finds(select_selector, name)
        if name:
            options[0].click()
        else:
            options[_id].click()

    def scroll_table(
        self, table_function, row=-1, wait_time=2, align_top: bool = True
    ):
        logger.info("scroll the table")
        table_before = table_function()
        timestamp = time.time() + wait_time
        self.d.execute_script(
            "arguments[0].scrollIntoView(arguments[1])",
            table_function()[row],
            align_top,
        )
        while time.time() < timestamp:
            time.sleep(0.5)
            if table_function() != table_before:
                return True
        return False

    def snackbar_message(self, parent):
        return parent.find(self.snackbar_message_element.selector).text

    def wait_snackbar_message(self, text, wait=5):
        return self.wait_text_appear(
            self.snackbar_message_element.selector, text, wait_time=wait
        )

    def wait_no_snackbar(self, wait=15):
        return self.wait_not_exist(
            self.snackbar_message_element.selector, wait_time=wait
        )

    def wait_no_progress(self, wait_time=5):
        self.wait_not_exist(self.progress_bar, wait_time=wait_time)

    @staticmethod
    def click_to_element(element, wait_time: int = 10):
        logger.info(f"try to click by element {element}")
        timestamp = time.time() + wait_time
        while time.time() < timestamp:
            try:
                element.click()
                break
            except (WebDriverException, TimeoutException):
                time.sleep(1)

    def move_to(self, element, align_to_top: bool = True):
        self.d.execute_script(
            "arguments[0].scrollIntoView(arguments[1]);", element, align_to_top
        )
        return element

    def get_blob_from_js(self, href):
        script = f"""
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '{href}', false);
        xhr.overrideMimeType('text\/plain; charset=x-user-defined');
        xhr.send(null);
        const reader = new FileReader();
        reader.addEventListener('loadend', (e) => {{
          const text = e.srcElement.result;
          console.warn(text);
          window.csvText = text
        }});
        const blob = new Blob([xhr.responseText], {{type: "text/plain"}})
        console.warn(reader.readAsText(blob));
        """  # noqa
        self.d.execute_script(script)
        _window_csv_text = "return window.csvText;"
        return self.d.execute_script(_window_csv_text)

    def check_alert(self):
        logger.info("check text in the alert window")
        alert = self.d.switch_to_alert()
        text = alert.text
        alert.accept()
        return text

    def select_element_w_text(self, elements: [WebElement], text: str):
        logger.info(f"Select element with text {text}")
        for el in elements:
            if el.text.find(text) != -1:
                return el
        return None
