"""
02_Pydantic_Validation - URL Validation
Enforcing operational syntax rules on downstream scraping destinations.
"""
from pydantic import BaseModel, HttpUrl, ValidationError


class ScrapingTarget(BaseModel):
    source_name: str
    target_url: HttpUrl


try:
    target = ScrapingTarget(source_name="DummyJSON",
                            target_url="[https://dummyjson.com/recipes](https://dummyjson.com/recipes)")
    print(f"Target URL Validated: {target.target_url}")

    # Missing scheme error verification
    ScrapingTarget(source_name="Malformed", target_url="ftp://corrupted-endpoint")
except ValidationError as e:
    print(f"\nURL Infrastructure Guard Intercepted Error:\n{e}")