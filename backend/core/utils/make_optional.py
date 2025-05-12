from pydantic import BaseModel, create_model
from typing import Optional, Type


def make_optional(model: Type[BaseModel]) -> Type[BaseModel]:
    optional_fields = {
        field_name: (Optional[field.type_], None)
        for field_name, field in model.__fields__.items()
    }
    return create_model(f"Partial{model.__name__}", **optional_fields)