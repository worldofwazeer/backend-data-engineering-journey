"""
02_Pydantic_Validation - Optional Fields
Handling missing keys and dynamic structural null states gracefully.
"""
from typing import Optional
from pydantic import BaseModel

class UserLog(BaseModel):
    session_id: str
    user_id: int
    # Python 3.10+ / modern Pydantic structural null handling
    referral_code: Optional[str] = None
    meta_tags: list[str] = []

# Payload missing 'referral_code' entirely
stripped_payload = {"session_id": "sess_8834", "user_id": 404}

validated_log = UserLog(**stripped_payload)
print(f"Parsed Stream State: Referral Code = {validated_log.referral_code}")
print(f"Parsed Stream State: Default List initialized = {validated_log.meta_tags}")