# tests/e2e/test_e2e.py

import pytest
from playwright.sync_api import expect


@pytest.mark.e2e
def test_hello_world(page, fastapi_server):
    """Homepage should display 'Hello World' in the h1 tag."""
    page.goto('http://localhost:8000')
    assert page.inner_text('h1') == 'Hello World'


@pytest.mark.e2e
def test_calculator_add(page, fastapi_server):
    """Add button should return the correct sum."""
    page.goto('http://localhost:8000')
    page.fill('#a', '10')
    page.fill('#b', '5')
    page.click('button:text("Add")')
    expect(page.locator('#result')).to_have_text('Result: 15')


@pytest.mark.e2e
def test_calculator_divide_by_zero(page, fastapi_server):
    """Dividing by zero should display an error message."""
    page.goto('http://localhost:8000')
    page.fill('#a', '10')
    page.fill('#b', '0')
    page.click('button:text("Divide")')
    expect(page.locator('#result')).to_have_text('Error: Cannot divide by zero!')


@pytest.mark.e2e
def test_calculator_subtract(page, fastapi_server):
    """Subtract button should return the correct difference."""
    page.goto('http://localhost:8000')
    page.fill('#a', '10')
    page.fill('#b', '4')
    page.click('button:text("Subtract")')
    expect(page.locator('#result')).to_have_text('Result: 6')


@pytest.mark.e2e
def test_calculator_multiply(page, fastapi_server):
    """Multiply button should return the correct product."""
    page.goto('http://localhost:8000')
    page.fill('#a', '10')
    page.fill('#b', '4')
    page.click('button:text("Multiply")')
    expect(page.locator('#result')).to_have_text('Result: 40')
