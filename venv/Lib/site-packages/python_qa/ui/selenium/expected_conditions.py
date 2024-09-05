from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException,
)
from selenium.webdriver.support.expected_conditions import (
    visibility_of_element_located,
)


class animation_ended:
    """
    An expectation for checking that element animation is ended.

    Returns WebElement once it is located.
    """

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        animating = _find_element(driver, self.locator).get_attribute(
            "data-animating"
        )
        return animating == "false"


class element_located_with_text:
    """
    An expectation for checking that there is an element in DOM with given text
    in it.

    Returns WebElement once it is located.
    """

    def __init__(self, locator, text):
        if str(locator[1]).endswith("]"):
            selector = locator[1][:-1] + f" and contains(node(), '{text}')]"
        else:
            selector = locator[1] + f"[contains(node(), '{text}')]"
        self.locator = (locator[0], selector)

    def __call__(self, driver):
        return _find_element(driver, self.locator)


class element_with_text:
    """
    An expectation for checking that there is an element in DOM with given text
    in it.

    Returns WebElement once it is located.
    """

    def __init__(self, element, text):
        self.element = element
        self.text = text

    def __call__(self, driver):
        return self.element.text == self.text


class number_of_all_elements_located(object):
    """An expectation for checking that there is at least given number of
    elements present on a web page.
    locator is used to find the element
    returns the list of WebElements once they are located
    """

    def __init__(self, locator, number):
        self.locator = locator
        self.number = number

    def __call__(self, driver):
        elements = _find_elements(driver, self.locator)
        if len(elements) >= self.number:
            return elements


class presence_element_to_be_clickable:
    """An Expectation for checking an element is visible and enabled such that
    you can click it."""

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            element = visibility_of_element_located(self.locator)(driver)
            if element and element.is_enabled():
                return element
            return False
        except StaleElementReferenceException:
            return False


def _find_element(driver, by):
    """Looks up an element. Logs and re-raises ``WebDriverException``
    if thrown."""
    try:
        return driver.find_element(*by)
    except NoSuchElementException as e:
        raise e
    except WebDriverException as e:
        raise e


def _find_elements(driver, by):
    try:
        return driver.find_elements(*by)
    except WebDriverException as e:
        raise e
