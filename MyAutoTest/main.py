import base64
import io
import re
import asyncio
import time

from PIL import Image
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright, expect, Playwright, PageAssertions
from selenium import webdriver


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





if __name__ == '__main__':
    pass
    # driver = webdriver.Chrome()
    # driver.get("https://www.baidu.com")
    # time.sleep(3)
    # kw = driver.find_element("xpath", "//*[@id='kw']")
    # driver.refresh()
    # kw.send_keys("selenium")
    # time.sleep(3)
    # driver.quit()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        page.goto("https://www.baidu.com")
        page.locator("//*[text()='设置']").nth(1).hover()
        expect(page).to_have_title()
        # page.get_by_text("设置").nth(1).hover()
        # page.locator("//*[@id='kw']")
        page.wait_for_timeout(3000)
