from datetime import datetime
from pydantic import (
    BaseModel,
    field_validator,
    Field,
    field_serializer
    
)


class BasePersonSchema(BaseModel):
    name: str = Field(
        ...,
        description="Enter persons name"
        )

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) > 32:
            raise ValueError(
                "Name must not exceed 32 characters"
            )
        if not value.isalpha():
            raise ValueError(
                "Name must contains only alphabetic characters"
            )
        return value

    @field_serializer("name")
    def serialize_name(value):
        return value.title()
    

class PersonResponseSchema(BasePersonSchema):
    id: int = Field(
        ...,
        description="Unique user identifier"
    )
    created_at: datetime = Field(
        ...,
        description="Record creation timestamp"
    )
    updated_at: datetime = Field(
        ...,
        description="Record updating timestamp"
    )
    
class PersonCreateSchema(BasePersonSchema):
    pass
    

class PersonUpdateSchema(BasePersonSchema):
    pass
    