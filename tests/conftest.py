import pytest

from feuersoftware.api import BASE_URL, FeuersoftwareAPI

TEST_TOKEN = "test-token-1234"


@pytest.fixture
def api():
    """A FeuersoftwareAPI instance with a dummy token, ready to hit mocked URLs."""
    return FeuersoftwareAPI(TEST_TOKEN)


@pytest.fixture
def base_url():
    return BASE_URL
