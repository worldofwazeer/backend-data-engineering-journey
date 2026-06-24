"""
02_Pydantic_Validation - Field Constraints
Enforcing boundaries on numerical and string metadata values.
"""
from pydantic import BaseModel, Field, ValidationError

class ProductInventory(BaseModel):
    product_id: int
    # Enforcing string length constraints and positive boundary ranges
    sku_code: str = Field(..., min_length=5, max_length=12)
    unit_price: float = Field(..., gt=0.0)
    stock_level: int = Field(..., ge=0)

invalid_payload = {"product_id": 99, "sku_code": "ABC", "unit_price": -5.50, "stock_level": -1}

try:
    ProductInventory(**invalid_payload)
except ValidationError as e:
    print(f"Captured Constraint Violations:\n{e}")