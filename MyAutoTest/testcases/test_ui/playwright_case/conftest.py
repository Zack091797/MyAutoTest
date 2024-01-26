import pytest
import asyncio
from _pytest.config.argparsing import Parser
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

play = None
browser = None
context = None


@pytest.fixture(scope="session", name="context")
def init_browserContext(request):
    global play, browser, context
    browserType = request.config.getoption("--SyncOrAsync")
    if browserType == "sync":
        play = sync_playwright().start()
        browser = play.chromium.launch(headless=False)
        context = browser.new_context()
        return context
    elif browserType == "async":
        async def get_browserContext():
            play_async = await async_playwright().start()
            browser = await play_async.chromium.launch(headless=False)
            context = await browser.new_context()
            return context

        return get_browserContext()


@pytest.fixture(scope="session", autouse=True)
def close_browserContext(request):
    yield
    global play, browser, context
    browserType = request.config.getoption("--SyncOrAsync")
    if browserType == "sync":
        context.close()
        browser.close()
        play.stop()
        context = None
        browser = None
        play = None
#     elif browserType == "async":
#         async def close_resource():
#             # await context.close()
#             # await browser.close()
#             await play.stop()
#             # await context = None
#             # await browser = None


@pytest.hookimpl
def pytest_addoption(parser: Parser):
    parser.addoption("--SyncOrAsync",
                     action="store",
                     default="sync",
                     type=str,
                     choices=["sync", "async"],
                     help="设置playwright的sync或async版本，默认sync")
