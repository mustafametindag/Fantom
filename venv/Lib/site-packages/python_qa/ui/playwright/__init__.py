from playwright.sync_api import Locator

from common.logging import logger


# ToDo: check is module install
class BaseElement:
    def __init__(self, selector: str, instance=None):
        self.selector = selector
        self.instance = instance

    def __get__(self, instance, owner):
        logger.info(f"Element requested: {self.selector}")
        self.instance = instance
        return self

    def __call__(self, *args, **kwargs) -> Locator:
        if "page" in dir(self.instance):
            logger.info(
                f"Search for an element by: {self.selector} "
                f"with parameters: {args}, {kwargs}"
            )
            return self.instance.page.locator(self.selector, *args, **kwargs)
