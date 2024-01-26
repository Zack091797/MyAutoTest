
class TestPlaywrightDemo:
    def test_playwright_demo(self, context):
        page = context.new_page()
        page.goto("https://www.baidu.com")
        page.wait_for_timeout(3000)
