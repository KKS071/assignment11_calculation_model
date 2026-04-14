# tests/integration/test_calculation_schema.py

"""Integration tests for Calculation Pydantic schemas."""

import pytest
from uuid import uuid4
from pydantic import ValidationError
from app.schemas.calculation import (
    CalculationType,
    CalculationBase,
    CalculationCreate,
    CalculationUpdate,
    CalculationResponse,
)


def test_calculation_type_enum_values():
    assert CalculationType.ADDITION.value == "addition"
    assert CalculationType.SUBTRACTION.value == "subtraction"
    assert CalculationType.MULTIPLICATION.value == "multiplication"
    assert CalculationType.DIVISION.value == "division"


def test_calculation_base_valid_addition():
    calc = CalculationBase(**{"type": "addition", "inputs": [10.5, 3, 2]})
    assert calc.type == CalculationType.ADDITION
    assert calc.inputs == [10.5, 3, 2]


def test_calculation_base_valid_subtraction():
    calc = CalculationBase(**{"type": "subtraction", "inputs": [20, 5.5]})
    assert calc.type == CalculationType.SUBTRACTION
    assert calc.inputs == [20, 5.5]


def test_calculation_base_case_insensitive_type():
    for type_variant in ["Addition", "ADDITION", "AdDiTiOn"]:
        calc = CalculationBase(**{"type": type_variant, "inputs": [1, 2]})
        assert calc.type == CalculationType.ADDITION


def test_calculation_base_invalid_type():
    with pytest.raises(ValidationError) as exc_info:
        CalculationBase(**{"type": "modulus", "inputs": [10, 3]})
    assert any("Type must be one of" in str(err) for err in exc_info.value.errors())


def test_calculation_base_inputs_not_list():
    with pytest.raises(ValidationError) as exc_info:
        CalculationBase(**{"type": "addition", "inputs": "not a list"})
    assert any("Input should be a valid list" in str(err) for err in exc_info.value.errors())


def test_calculation_base_insufficient_inputs():
    with pytest.raises(ValidationError) as exc_info:
        CalculationBase(**{"type": "addition", "inputs": [5]})
    assert len(exc_info.value.errors()) > 0


def test_calculation_base_empty_inputs():
    with pytest.raises(ValidationError) as exc_info:
        CalculationBase(**{"type": "multiplication", "inputs": []})
    assert len(exc_info.value.errors()) > 0


def test_calculation_base_division_by_zero():
    with pytest.raises(ValidationError) as exc_info:
        CalculationBase(**{"type": "division", "inputs": [100, 0]})
    assert any("Cannot divide by zero" in str(err) for err in exc_info.value.errors())


def test_calculation_base_division_by_zero_in_middle():
    with pytest.raises(ValidationError) as exc_info:
        CalculationBase(**{"type": "division", "inputs": [100, 5, 0, 2]})
    assert any("Cannot divide by zero" in str(err) for err in exc_info.value.errors())


def test_calculation_base_division_zero_numerator_ok():
    calc = CalculationBase(**{"type": "division", "inputs": [0, 5, 2]})
    assert calc.inputs[0] == 0


def test_calculation_create_valid():
    user_id = uuid4()
    calc = CalculationCreate(**{
        "type": "multiplication", "inputs": [2, 3, 4], "user_id": str(user_id)
    })
    assert calc.type == CalculationType.MULTIPLICATION
    assert calc.inputs == [2, 3, 4]
    assert calc.user_id == user_id


def test_calculation_create_missing_user_id():
    with pytest.raises(ValidationError) as exc_info:
        CalculationCreate(**{"type": "addition", "inputs": [1, 2]})
    assert any("user_id" in str(err) for err in exc_info.value.errors())


def test_calculation_create_invalid_user_id():
    with pytest.raises(ValidationError):
        CalculationCreate(**{
            "type": "subtraction", "inputs": [10, 5], "user_id": "not-a-valid-uuid"
        })


def test_calculation_update_valid():
    calc = CalculationUpdate(**{"inputs": [42, 7]})
    assert calc.inputs == [42, 7]


def test_calculation_update_all_fields_optional():
    calc = CalculationUpdate(**{})
    assert calc.inputs is None


def test_calculation_update_insufficient_inputs():
    with pytest.raises(ValidationError) as exc_info:
        CalculationUpdate(**{"inputs": [5]})
    assert len(exc_info.value.errors()) > 0


def test_calculation_response_valid():
    from datetime import datetime
    data = {
        "id": str(uuid4()),
        "user_id": str(uuid4()),
        "type": "addition",
        "inputs": [10, 5],
        "result": 15.0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    calc = CalculationResponse(**data)
    assert calc.result == 15.0
    assert calc.type == CalculationType.ADDITION


def test_calculation_response_missing_result():
    from datetime import datetime
    data = {
        "id": str(uuid4()),
        "user_id": str(uuid4()),
        "type": "multiplication",
        "inputs": [2, 3],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationResponse(**data)
    assert any("result" in str(err) for err in exc_info.value.errors())


def test_multiple_calculations_with_different_types():
    user_id = uuid4()
    calcs_data = [
        {"type": "addition", "inputs": [1, 2, 3], "user_id": str(user_id)},
        {"type": "subtraction", "inputs": [10, 3], "user_id": str(user_id)},
        {"type": "multiplication", "inputs": [2, 3, 4], "user_id": str(user_id)},
        {"type": "division", "inputs": [100, 5], "user_id": str(user_id)},
    ]
    calcs = [CalculationCreate(**data) for data in calcs_data]
    assert len(calcs) == 4
    assert calcs[0].type == CalculationType.ADDITION
    assert calcs[1].type == CalculationType.SUBTRACTION
    assert calcs[2].type == CalculationType.MULTIPLICATION
    assert calcs[3].type == CalculationType.DIVISION


def test_schema_with_large_numbers():
    calc = CalculationBase(**{"type": "multiplication", "inputs": [1e10, 1e10, 1e10]})
    assert all(isinstance(x, float) for x in calc.inputs)


def test_schema_with_negative_numbers():
    calc = CalculationBase(**{"type": "addition", "inputs": [-5, -10, 3.5]})
    assert calc.inputs == [-5, -10, 3.5]


def test_schema_with_mixed_int_and_float():
    calc = CalculationBase(**{"type": "subtraction", "inputs": [100, 23.5, 10, 6.7]})
    assert len(calc.inputs) == 4
