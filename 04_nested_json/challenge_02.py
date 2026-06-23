import logging
import requests
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field, EmailStr, HttpUrl, ValidationError, ConfigDict
from pydantic.alias_generators import to_camel
from itertools import chain

# =====================================================================
# 0. SETUP: LOGGING & PYDANTIC MODELS (The "Magic" Way)
# =====================================================================
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


# 🪄 THE MAGIC: This BaseSchema automatically converts all camelCase API data into snake_case!
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


# 1. EXTRACT

def extract_from_api(url: str) -> list[dict[str, Any]]:
    """Fetches raw JSON payloads from the target endpoint."""
    try:
        logger.info("[1/4] EXTRACTING: Hitting API endpoint...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json().get("products", [])

    except requests.exceptions.RequestException as error:
        logger.error(f"[1/4] EXTRACT FAILED: {error}")
        return []


# 2. VALIDATE

def validate_data(raw_products: list[dict[str, Any]]) -> list[Product]:
    """Passes raw dictionaries through Pydantic to ensure data integrity."""
    logger.info(f"[2/4] VALIDATING: Checking {len(raw_products)} raw records...")
    validated_records = []

    for product in raw_products:
        try:
            valid_product = Product.model_validate(product)
            validated_records.append(valid_product)
        except ValidationError as error:
            product_id = product.get("id", "Unknown")

            logger.warning(
                f"Dropping Product ID {product_id} due to schema violation. "
                f"Details:\n{error}"
            )

    return validated_records


# 3. TRANSFORM & FLATTEN

def flatten_single_product(product: Product) -> list[dict[str, Any]]:
    """Normalizes one Pydantic product object into flat rows (handling 1-to-Many reviews)."""

    # We must convert complex objects (HttpUrl, datetime) to strings for the database!
    base_info = {
        "product_id": product.id,
        "title": product.title,
        "category": product.category,
        "price": product.price,
        "stock": product.stock,
        "brand": product.brand,
        "tags": ", ".join(product.tags),
        "thumbnail_url": str(product.thumbnail),
        "created_at": product.meta.created_at.isoformat(),
    }

    if not product.reviews:
        return [{
            **base_info,
            "review_rating": None,
            "review_comment": None,
            "reviewer_email": None,
            "review_date": None
        }]
    else:
        return [
            {
                **base_info,
                "review_rating": review.rating,
                "review_comment": review.comment,
                "reviewer_email": str(review.reviewer_email),
                "review_date": review.date.isoformat()
            }
            for review in product.reviews
        ]

def transform_data(validated_products: list[Product]) -> list[dict[str, Any]]:
    """Iterates through all valid products and runs the flattening logic."""
    logger.info("[3/4] TRANSFORMING: Normalizing nested data into flat rows...")
    # return list(chain.from_iterable(flatten_single_product(product) for product in validated_products))

    flattened_dataset = []

    for product in validated_products:
        flattened_dataset.extend(flatten_single_product(product))

    return flattened_dataset


# =====================================================================
# 4. LOAD (PostgreSQL)
# =====================================================================
def save_to_postgre(dataset: list[dict[str, Any]], db_credentials: dict) -> None:
    """Uses execute_values for high-performance bulk insertion into PostgreSQL."""
    if not dataset:
        logger.warning("[4/4] LOAD: No data to save.")
        return

    logger.info(f"[4/4] LOAD: Connecting to PostgreSQL to insert {len(dataset)} rows...")

    # Extract column names dynamically from the first dictionary
    columns = list(dataset[0].keys())
    columns_str = ", ".join(columns)

    # Convert dictionaries to a list of tuples for psycopg2
    values = [[row[col] for col in columns] for row in dataset]

    # Create the SQL Query
    # The 'ON CONFLICT DO NOTHING' prevents the script from crashing if you scrape the same product twice!
    insert_query = f"""
        INSERT INTO product_reviews ({columns_str})
        VALUES %s
        ON CONFLICT (product_id, reviewer_email) DO NOTHING;
    """

    try:
        # 1. Connect to the database
        conn = psycopg2.connect(**db_credentials)
        cursor = conn.cursor()

        # 2. Execute bulk insert
        execute_values(cursor, insert_query, values)

        # 3. Commit and close
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("[SUCCESS] Data successfully committed to PostgreSQL database!")

    except Exception as e:
        logger.error(f"[FATAL] PostgreSQL Insertion Failed: {e}")


# =====================================================================
# MAIN ORCHESTRATOR
# =====================================================================
def main():
    API_URL = "https://dummyjson.com/products"

    # Replace these with your actual PostgreSQL database credentials!
    DB_CREDENTIALS = {
        "dbname": "your_database_name",
        "user": "your_username",
        "password": "your_password",
        "host": "localhost",
        "port": "5432"
    }

    # 1. Extract
    raw_data = extract_from_api(API_URL)

    # 2. Validate
    valid_data = validate_data(raw_data)

    # 3. Transform
    final_dataset = transform_data(valid_data)

    # 4. Load
    # NOTE: You must create the 'product_reviews' table in pgAdmin/SQL before running this!
    if final_dataset:
        save_to_postgre(final_dataset, DB_CREDENTIALS)


if __name__ == "__main__":
    main()