"""
02_Pydantic_Validation - Field Aliases
Mapping incoming external naming schemes to clean pythonic variables.
"""
from pydantic import BaseModel, Field

class ExternalUserRecord(BaseModel):
    # Mapping API camelCase properties cleanly to Python snake_case
    user_id: int = Field(..., alias="userId")
    first_name: str = Field(..., alias="firstName")
    account_status: str = Field(..., alias="accountStatus")

# Sample external API payload response representation
api_response = {
    "userId": 2045,
    "firstName": "Ibrahim",
    "accountStatus": "active"
}

mapped_record = ExternalUserRecord(**api_response)
print(f"Alias Translation Complete -> Python Variable Name: {mapped_record.first_name}")