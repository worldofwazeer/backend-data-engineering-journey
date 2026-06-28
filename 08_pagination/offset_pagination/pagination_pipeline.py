import requests
import logging
from typing import Any
from pydantic import (BaseModel, Field, EmailStr, HttpUrl, ValidationError, ConfigDict)
from pydantic.alias_generators import to_camel
from datetime import datetime

# SETUP: LOGGING & PYDANTIC MODELS
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt="%d-%b-%y %H:%M:%S",
                    # filename="basic.log"
                    )
logger = logging.getLogger("ETL_PRACTICE")


class BaseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class Dimensions(BaseSchema):
    width: float = Field(gt=0)
    height: float = Field(gt=0)
    depth: float = Field(gt=0)


class Review(BaseSchema):
    rating: float = Field(ge=0)
    comment: str = Field(min_length=1)
    date: datetime
    reviewer_email: EmailStr
    reviewer_name: str = Field(min_length=1)


class Meta(BaseSchema):
    created_at: datetime
    updated_at: datetime
    barcode: str = Field(min_length=1)
    qr_code: HttpUrl


class Product(BaseSchema):
    id: int = Field(gt=0)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    category: str = Field(min_length=1)
    price: float = Field(gt=0)
    discount_percentage: float = Field(ge=0)
    rating: float = Field(ge=0)
    stock: int = Field(ge=0)
    tags: list[str]
    brand: str | None = None
    sku: str = Field(min_length=1)
    weight: float = Field(gt=0)
    warranty_information: str = Field(min_length=1)
    shipping_information: str = Field(min_length=1)
    availability_status: str = Field(min_length=1)
    return_policy: str = Field(min_length=1)
    minimum_order_quantity: int = Field(gt=0)

    images: list[HttpUrl]
    thumbnail: HttpUrl
    dimensions: Dimensions
    meta: Meta
    reviews: list[Review] = Field(default_factory=list)


def extract_page(skip: int, limit: int) -> list[dict[str, Any]]:
    try:
        url = "https://dummyjson.com/products"
        logger.info("[1/5] EXTRACT pages for: %s", url)

        params = {
            "limit": limit,
            "skip": skip
        }
        response = requests.get(url, timeout=15, params=params)
        response.raise_for_status()
        return response.json().get("products", [])
    except requests.exceptions.RequestException as e:
        logger.error(e)
        return []


def validate_products(raw_products: list[dict[str, Any]]) -> list[Product]:
    logger.info("[2/5] VALIDATE: %d products", len(raw_products))
    valid = []

    for item in raw_products:
        try:
            valid.append(Product.model_validate(item))
        except ValidationError:
            continue

    return valid


def transform(products: list[Product]) -> list[dict[str, Any]]:
    logger.info("[3/5] TRANSFORM: %d products", len(products))
    return [
        {
            "id": p.id,
            "title": p.title,
            "price": p.price,
            "thumbnail": str(p.thumbnail),
        }
        for p in products
    ]


def fetch_all_products() -> list[dict[str, Any]]:
    limit = 20
    skip = 0
    final_dataset = []

    logger.info("Starting Ingestion Pipeline...")

    while True:
        # 1. Extract
        products = extract_page(skip, limit)
        if not products:
            logger.info("🏁 No more records found. Ingestion complete.")
            break

        # 2. Validate
        validated = validate_products(products)

        # 3. Transform
        transformed = transform(validated)
        final_dataset.extend(transformed)

        logger.info(
            "Processed page (skip=%d): %d rows | Running total: %d",
            skip,
            len(transformed),
            len(final_dataset)
        )

        skip += limit

    return final_dataset

def main():
    data = fetch_all_products()

    print(f"Total records: {len(data)}")
    print("Sample:", data[0] if data else None)

if __name__ == "__main__":
    main()

