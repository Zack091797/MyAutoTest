import base64
import io
import re
import asyncio
import time

from PIL import Image
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright, expect, Playwright


def image_to_base64_native(image_path):
    with open(image_path, mode='rb') as image_file:
        encoded = base64.b64encode(image_file.read())
    return encoded.decode('utf-8')


def image_to_base64_PIL(imagePath, save_format='png'):
    with Image.open(imagePath) as img:
        output_buffer = io.BytesIO()
        img.save(output_buffer, format=save_format)
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data).decode('utf-8')
    return base64_str


def base64_to_image_PIL(base64_str, img_path=None):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = io.BytesIO(byte_data)
    with Image.open(image_data) as img:
        if img_path:
            img.save(img_path)
    return img


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.baidu.com")
    page.locator("#kw").fill("playwright")
    # page.pause()  # 断点
    page.get_by_role("button", name="百度一下").click()
    page.wait_for_timeout(3000)

    # ---------------------
    context.close()
    browser.close()


if __name__ == '__main__':
    pass

    with sync_playwright() as playwright:
        run(playwright)

    # with sync_playwright() as play:
    #     browser = play.chromium.launch(headless=False, slow_mo=500)
    #     context = browser.new_context()
    #
    #     page1 = context.new_page()
    #     page2 = context.new_page()
    #
    #     page1.goto("https://www.baidu.com")
    #     # page2.goto("https://163.com")
    #
    #     page1.wait_for_timeout(5000)
    #     page2.wait_for_timeout(3000)
    #
    #     page1.close()
    #     page2.close()

    # with sync_playwright() as play:
    #     browser = play.chromium.launch(headless=False, slow_mo=500)
    #     context = browser.new_context()
    #     page = context.new_page()
    #     page.goto("https://www.baidu.com")
    #     print(page.title())
    #     page.fill("#kw", "playwright")
    #     page.wait_for_timeout(5000)
    #     page.click("#su")
    #     time.sleep(3)
    #     page.close()
    #
    #     page.get_by_role()
    #     page.locator().click()
    #     expect().to_be_visible()
    #
    #     page.get_by_text()
    #     page.locator()
    #     page.frame_locator()
    #     page.frame()
    #     page.hover()
    #     page.wait_for_load_state()
    #     page.wait_for_timeout()
    #     page.screenshot()
    #     with page.expect_file_chooser() as efc_info:
    #         pass
    #
    #     with context.expect_page() as cep_info:
    #         pass
    #
    #     context.on()

    # async def main():
    #     async with async_playwright() as play:
    #         browser = await play.chromium.launch(headless=False)
    #         page = await browser.new_page()
    #         page.get_by_role()
    #         await page.goto("https://www.baidu.com")
    #         print(await page.title())
    #         await browser.close()
    # asyncio.run(main())

    # play = sync_playwright().start()
    # browser = play.chromium.launch(headless=False)
    # page = browser.new_page()
    # page.goto("https://www.baidu.com")
    # browser.close()
    # play.stop()
