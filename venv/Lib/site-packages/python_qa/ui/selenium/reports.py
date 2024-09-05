import pytest
import allure
from ...logging.logging import Logging
logger = Logging.logger


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        try:
            if "driver" in item.fixturenames:
                driver = item.funcargs["driver"]
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
                allure.attach(
                    "\n".join(map(str, driver.get_log("browser"))),
                    name="console log",
                    attachment_type=allure.attachment_type.TEXT,
                )
        except Exception as e:
            logger.info(f"Fail to take screenshot: {e}")
