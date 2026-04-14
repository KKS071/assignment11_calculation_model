# app/schemas/calculation.py
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict, model_validator, field_validator
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class CalculationType(str, Enum):
    """Valid calculation types. Inherits from str for JSON serialization."""
    ADDITION = "addition"
    SUBTRACTION = "subtraction"
    MULTIPLICATION = "multiplication"
    DIVISION = "division"


class CalculationBase(BaseModel):
    """Base schema with shared fields for all calculation requests."""

    type: CalculationType = Field(..., description="Type of calculation", examples=["addition"])
    inputs: List[float] = Field(
        ..., description="Numbers to calculate", examples=[[10.5, 3, 2]], min_length=2
    )

    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, v):
        """Normalize type to lowercase and reject unsupported values."""
        allowed = {e.value for e in CalculationType}
        if not isinstance(v, str) or v.lower() not in allowed:
            raise ValueError(f"Type must be one of: {', '.join(sorted(allowed))}")
        return v.lower()

    @field_validator("inputs", mode="before")
    @classmethod
    def check_inputs_is_list(cls, v):
        """Reject inputs that are not a list."""
        if not isinstance(v, list):
            raise ValueError("Input should be a valid list")
        return v

    @model_validator(mode='after')
    def validate_inputs(self) -> "CalculationBase":
        """Require at least 2 inputs; reject division by zero in denominators."""
        if len(self.inputs) < 2:
            raise ValueError("At least two numbers are required for calculation")
        if self.type == CalculationType.DIVISION:
            if any(x == 0 for x in self.inputs[1:]):
                raise ValueError("Cannot divide by zero")
        return self

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {"type": "addition", "inputs": [10.5, 3, 2]},
                {"type": "division", "inputs": [100, 2]},
            ]
        },
    )


class CalculationCreate(CalculationBase):
    """Schema for creating a new calculation, requires user_id."""
    user_id: UUID = Field(
        ...,
        description="UUID of the owning user",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "addition",
                "inputs": [10.5, 3, 2],
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
            }
        }
    )


class CalculationUpdate(BaseModel):
    """Schema for updating a calculation's inputs (all fields optional)."""
    inputs: Optional[List[float]] = Field(
        None, description="Updated inputs", examples=[[42, 7]], min_length=2
    )

    @model_validator(mode='after')
    def validate_inputs(self) -> "CalculationUpdate":
        """Validate inputs only when they are being updated."""
        if self.inputs is not None and len(self.inputs) < 2:
            raise ValueError("At least two numbers are required for calculation")
        return self

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"inputs": [42, 7]}},
    )


class CalculationResponse(CalculationBase):
    """Schema returned when reading a calculation from the database."""
    id: UUID = Field(..., description="Calculation UUID", examples=["123e4567-e89b-12d3-a456-426614174999"])
    user_id: UUID = Field(..., description="Owning user UUID", examples=["123e4567-e89b-12d3-a456-426614174000"])
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    result: float = Field(..., description="Computed result", examples=[15.5])

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174999",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "type": "addition",
                "inputs": [10.5, 3, 2],
                "result": 15.5,
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00",
            }
        },
    )
