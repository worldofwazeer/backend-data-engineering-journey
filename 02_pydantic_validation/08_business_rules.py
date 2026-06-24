"""
02_Pydantic_Validation - Custom Business Logic Rules
Writing localized functional field state validation hooks.
"""
from pydantic import BaseModel, Field, field_validator, ValidationError

class FinancialTransaction(BaseModel):
    transaction_id: str
    currency: str = Field(..., min_length=3, max_length=3)
    amount: float

    @field_validator('currency')
    @classmethod
    def ensure_uppercase_currency(cls, value: str) -> str:
        """Enforces uppercase requirements prior to internal parsing updates."""
        if not value.isupper():
            raise ValueError("Currency formatting specification must be strict uppercase.")
        return value

try:
    # Triggering custom validation error via lowercase tracking variables
    FinancialTransaction(transaction_id="tx_991", currency="usd", amount=1500.00)
except ValidationError as e:
    print(f"Business Rule Execution Blocked Ingestion:\n{e}")