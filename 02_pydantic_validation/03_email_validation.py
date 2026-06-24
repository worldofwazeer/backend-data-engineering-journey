"""
02_Pydantic_Validation - Email Validation
Validating communication metadata layers securely.
"""
# Note: Requires 'pip install "pydantic[email]"'
from pydantic import BaseModel, EmailStr, ValidationError


class UserProfile(BaseModel):
    username: str
    contact_email: EmailStr


try:
    user = UserProfile(username="wazeer_dev", contact_email="engineering@wazeer.com")
    print(f"Valid Email Parsed: {user.contact_email}")

    # Triggering intentional validation crash
    UserProfile(username="bad_actor", contact_email="invalid-email-format")
except ValidationError as e:
    print(f"\nEmail Syntax Guard Intercepted Error:\n{e}")