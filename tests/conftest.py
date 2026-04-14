# tests/conftest.py
import subprocess
import time
import pytest
from playwright.sync_api import sync_playwright
import requests


@pytest.fixture(scope='session')
def fastapi_server():
    """Start the FastAPI server before E2E tests; stop it after."""
    process = subprocess.Popen(['python', 'main.py'])
    server_url = 'http://127.0.0.1:8000/'
    timeout = 30
    start_time = time.time()
    server_up = False

    print("Starting FastAPI server...")
    while time.time() - start_time < timeout:
        try:
            response = requests.get(server_url)
            if response.status_code == 200:
                server_up = True
                print("FastAPI server is up.")
                break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)

    if not server_up:
        process.terminate()
        raise RuntimeError("FastAPI server failed to start within timeout.")

    yield

    print("Shutting down FastAPI server...")
    process.terminate()
    process.wait()


@pytest.fixture(scope="session")
def playwright_instance_fixture():
    """Manage Playwright lifecycle for the session."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance_fixture):
    """Launch a headless Chromium browser for the session."""
    browser = playwright_instance_fixture.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """Open a fresh browser page for each test."""
    page = browser.new_page()
    yield page
    page.close()
