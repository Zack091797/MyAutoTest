
class TestPlaywrightDemo:
    def test_playwright_demo(self, context):
        page = context.new_page()
        # page.goto("https://www.baidu.com")
        # page.locator("//span[@id='s-usersetting-top']").hover()
        # page.wait_for_timeout(3000)
        page.goto("https://www.runoob.com/")
        # page.get_by_text('【学习 Django】').scroll_into_view_if_needed()
        page.get_by_text('【学习 Django】').click()
        page.wait_for_timeout(3000)


