import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def client():
    """Provide a fresh TestClient and reset app state after each test."""
    original_activities = copy.deepcopy(app_module.activities)

    with TestClient(app_module.app) as client:
        yield client

    app_module.activities = original_activities
