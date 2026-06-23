import requests
import logging
from typing import Any
from pydantic import (BaseModel, Field, EmailStr, ValidationError, ConfigDict)
from pydantic.alias_generators import to_camel
from itertools import chain
import json
from tqdm.auto import tqdm


# SETUP: LOGGING & PYDANTIC MODELS
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt="%d-%b-%y %H:%M:%S",
                    # filename="basic.log"
                    )
logger = logging.getLogger(__name__)

class BaseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)     

class Geo(BaseSchema):
    lat: float
    lng: float

class Address(BaseSchema):
    street: str = Field(min_length=1)
    suite: str | None = None
    city: str = Field(min_length=1)
    zipcode: str = Field(min_length=1)
    geo: Geo

class Company(BaseSchema):
    name: str = Field(min_length=1)
    catch_phrase: str = Field(min_length=1)
    bs: str = Field(min_length=1)

class UserRecord(BaseSchema):
    id: int = Field(gt=0)
    name: str = Field(min_length=1)
    username: str = Field(min_length=1)
    email: EmailStr
    phone: str = Field(min_length=1)
    website: str | None = None

    address: Address
    company: Company | None = None

# 1. EXTRACT
def extract_from_api(url: str) -> list[dict[str, Any]]:
    try:
        logger.info("EXTRACTING: Hitting API endpoint")
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        user_record = response.json()
        if isinstance(user_record, list):
            return user_record
        else:
            logger.warning("API did not return a root array list as expected.")
            return []

    except requests.exceptions.RequestException as error:
        logger.warning(f"EXTRACTING FAILED: {error}")
        return []

# 2. VALIDATE

def validate_data_with_progress(raw_users: list[dict[str, Any]]) -> list[UserRecord]:
    # 1. The standard log leaves a permanent breadcrumb
    logger.info(f"[2/4] VALIDATION: Checking {len(raw_users)} records...")

    validated_users: list[UserRecord] = []

    # 2. tqdm.auto wraps the list to create the visual progress bar
    for item in tqdm(raw_users, desc="Validating Users", unit="user"):
        try:
            valid_user = UserRecord.model_validate(item)
            validated_users.append(valid_user)

        except ValidationError as error:
            # 3. The Walrus Operator safely attempts to grab the ID in one line!
            bad_id = uid if (uid := item.get("id")) else "Unknown"

            # 4. tqdm.write ensures the text prints safely ABOVE the progress bar
            # without breaking the visual animation.
            tqdm.write(
                f"⚠️ DROPPING ID {bad_id}: Schema violation. "
                f"Details: {error.errors()[0]['msg']}"  # Grabs just the specific error message
            )

    return validated_users


def flatten_single_user(user: UserRecord) -> dict[str, Any]:
    """Transforms a nested user object into a single flat dictionary safely."""

    # 1. Grab all the MANDATORY fields first
    flat_row = {

        "user_id": user.id,
        "name": user.name,
        "username": user.username,
        "email": str(user.email),
        "phone_number": user.phone,

        "street": user.address.street,
        "city": user.address.city,
        "zipcode": user.address.zipcode,
        "latitude": user.address.geo.lat,
        "longitude": user.address.geo.lng
    }

    # 2. SAFE EXTRACTION: Simple Optional Strings (Website & Suite)
    # If user.website exists, use it. Otherwise, use "N/A"
    flat_row["website"] = user.website if user.website else "N/A"
    flat_row["suite"] = user.address.suite if user.address.suite else "N/A"

    # 3. SAFE EXTRACTION: Nested Dictionaries (Company)
    if user.company:
        # If the company exists, grab its inner details
        flat_row["company_name"] = user.company.name
        flat_row["catch_phrase"] = user.company.catch_phrase
        flat_row["business_strategy"] = user.company.bs
    else:
        # If the company is missing (None), fill the columns with blank/N/A
        flat_row["company_name"] = "N/A"
        flat_row["catch_phrase"] = "N/A"
        flat_row["business_strategy"] = "N/A"

    return flat_row

def transform_data(validate_users: list[UserRecord]) -> list[dict[str, Any]]:
    logger.info("[TRANSFORMING]: Normalizing nested data into flat rows..")
    # return [
    #     flatten_single_user(user)
    #     for user in validate_users
    # ]
    return list(chain.from_iterable(flatten_single_user(data) for data in validate_users))

def main():
    API_URL = "https://jsonplaceholder.typicode.com/users"
    raw_data = extract_from_api(API_URL)
    valid_data = validate_data_with_progress(raw_data)
    final_data = transform_data(valid_data)

    logger.info(f"[SUCCESS]: Pipeline closed. {len(final_data)} records were successfully transformed.")

    if final_data:


        pretty_sample = json.dumps(final_data, indent=4)

        logger.info(f"Sample Record:\n{pretty_sample}")


if __name__ == "__main__":
    main()





