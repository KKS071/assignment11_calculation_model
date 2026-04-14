# tests/integration/test_calculation.py

"""
Integration tests for polymorphic Calculation models and the factory pattern.
"""

import pytest
import uuid

from app.models import (
    Calculation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
)


def dummy_user_id():
    """Generate a random UUID to use as a user_id in tests."""
    return uuid.uuid4()


# --- Individual calculation type tests ---

def test_addition_get_result():
    """Addition should sum all inputs."""
    inputs = [10, 5, 3.5]
    addition = Addition(user_id=dummy_user_id(), inputs=inputs)
    result = addition.get_result()
    assert result == sum(inputs), f"Expected {sum(inputs)}, got {result}"


def test_subtraction_get_result():
    """Subtraction should sequentially subtract from the first value."""
    inputs = [20, 5, 3]
    subtraction = Subtraction(user_id=dummy_user_id(), inputs=inputs)
    assert subtraction.get_result() == 12, "Expected 20 - 5 - 3 = 12"


def test_multiplication_get_result():
    """Multiplication should return the product of all inputs."""
    inputs = [2, 3, 4]
    multiplication = Multiplication(user_id=dummy_user_id(), inputs=inputs)
    assert multiplication.get_result() == 24, "Expected 2 * 3 * 4 = 24"


def test_division_get_result():
    """Division should sequentially divide from the first value."""
    inputs = [100, 2, 5]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    assert division.get_result() == 10, "Expected 100 / 2 / 5 = 10"


def test_division_by_zero():
    """Division should raise ValueError when a denominator is zero."""
    inputs = [50, 0, 5]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        division.get_result()


# --- Factory pattern tests ---

def test_calculation_factory_addition():
    """Factory should return an Addition instance for 'addition'."""
    inputs = [1, 2, 3]
    calc = Calculation.create(calculation_type='addition', user_id=dummy_user_id(), inputs=inputs)
    assert isinstance(calc, Addition), "Factory did not return an Addition instance."
    assert isinstance(calc, Calculation), "Addition should also be a Calculation instance."
    assert calc.get_result() == sum(inputs), "Incorrect addition result."


def test_calculation_factory_subtraction():
    """Factory should return a Subtraction instance for 'subtraction'."""
    inputs = [10, 4]
    calc = Calculation.create(calculation_type='subtraction', user_id=dummy_user_id(), inputs=inputs)
    assert isinstance(calc, Subtraction), "Factory did not return a Subtraction instance."
    assert calc.get_result() == 6, "Expected 10 - 4 = 6"


def test_calculation_factory_multiplication():
    """Factory should return a Multiplication instance for 'multiplication'."""
    inputs = [3, 4, 2]
    calc = Calculation.create(calculation_type='multiplication', user_id=dummy_user_id(), inputs=inputs)
    assert isinstance(calc, Multiplication), "Factory did not return a Multiplication instance."
    assert calc.get_result() == 24, "Expected 3 * 4 * 2 = 24"


def test_calculation_factory_division():
    """Factory should return a Division instance for 'division'."""
    inputs = [100, 2, 5]
    calc = Calculation.create(calculation_type='division', user_id=dummy_user_id(), inputs=inputs)
    assert isinstance(calc, Division), "Factory did not return a Division instance."
    assert calc.get_result() == 10, "Expected 100 / 2 / 5 = 10"


def test_calculation_factory_invalid_type():
    """Factory should raise ValueError for unsupported types."""
    with pytest.raises(ValueError, match="Unsupported calculation type"):
        Calculation.create(calculation_type='modulus', user_id=dummy_user_id(), inputs=[10, 3])


def test_calculation_factory_case_insensitive():
    """Factory should accept type strings regardless of case."""
    inputs = [5, 3]
    for calc_type in ['addition', 'Addition', 'ADDITION', 'AdDiTiOn']:
        calc = Calculation.create(calculation_type=calc_type, user_id=dummy_user_id(), inputs=inputs)
        assert isinstance(calc, Addition), f"Factory failed for case: {calc_type}"
        assert calc.get_result() == 8


# --- Input validation edge cases ---

def test_invalid_inputs_for_addition():
    """Addition should raise ValueError when inputs is not a list."""
    addition = Addition(user_id=dummy_user_id(), inputs="not-a-list")
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        addition.get_result()


def test_invalid_inputs_for_subtraction():
    """Subtraction should raise ValueError with fewer than two inputs."""
    subtraction = Subtraction(user_id=dummy_user_id(), inputs=[10])
    with pytest.raises(ValueError, match="Inputs must be a list with at least two numbers."):
        subtraction.get_result()


def test_invalid_inputs_for_multiplication():
    """Multiplication should raise ValueError with fewer than two inputs."""
    multiplication = Multiplication(user_id=dummy_user_id(), inputs=[5])
    with pytest.raises(ValueError, match="Inputs must be a list with at least two numbers."):
        multiplication.get_result()


def test_invalid_inputs_for_division():
    """Division should raise ValueError with fewer than two inputs."""
    division = Division(user_id=dummy_user_id(), inputs=[10])
    with pytest.raises(ValueError, match="Inputs must be a list with at least two numbers."):
        division.get_result()


def test_division_by_zero_in_middle():
    """Division should catch zero in any denominator position."""
    division = Division(user_id=dummy_user_id(), inputs=[100, 5, 0, 2])
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        division.get_result()


def test_division_by_zero_at_end():
    """Division should catch zero as the last input."""
    division = Division(user_id=dummy_user_id(), inputs=[50, 5, 0])
    with pytest.raises(ValueError, match="Cannot divide by zero."):
        division.get_result()


# --- Polymorphism tests ---

def test_polymorphic_list_of_calculations():
    """Different calculation types can live in the same list and produce correct results."""
    user_id = dummy_user_id()
    calculations = [
        Calculation.create('addition', user_id, [1, 2, 3]),
        Calculation.create('subtraction', user_id, [10, 3]),
        Calculation.create('multiplication', user_id, [2, 3, 4]),
        Calculation.create('division', user_id, [100, 5]),
    ]
    assert isinstance(calculations[0], Addition)
    assert isinstance(calculations[1], Subtraction)
    assert isinstance(calculations[2], Multiplication)
    assert isinstance(calculations[3], Division)

    results = [calc.get_result() for calc in calculations]
    assert results == [6, 7, 24, 20]


def test_polymorphic_method_calling():
    """Calling get_result() polymorphically should dispatch to the right subclass."""
    user_id = dummy_user_id()
    inputs = [10, 2]
    calc_types = ['addition', 'subtraction', 'multiplication', 'division']
    expected_results = [12, 8, 20, 5]

    for calc_type, expected in zip(calc_types, expected_results):
        calc = Calculation.create(calc_type, user_id, inputs)
        result = calc.get_result()
        assert result == expected, f"{calc_type}: expected {expected}, got {result}"
