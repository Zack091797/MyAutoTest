


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def locate(self, loc):
        return self.driver.find_element(*loc)

    def locate(self, loc, index=None):
        if index is None:
            return self.driver.find_elements(*loc)
        else:
            return self.driver.find_elements(*loc)[index]