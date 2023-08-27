import pytest


@pytest.fixture(scope="session", autouse=False)
def connect_sql():
    pass


@pytest.fixture(scope="session", autouse=False)
def close_sql():
    yield
    pass