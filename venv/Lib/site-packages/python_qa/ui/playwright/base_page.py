class BasePage:
    def click_and_get_request(self, el, url: str):
        with self.page.expect_request(url) as request_info:
            el.last.click()
        return request_info.value

    def click_and_get_response(self, el, url: str):
        with self.page.expect_response(url) as response_info:
            el.last.click()
        return response_info.value
