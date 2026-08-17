"""
01_Python_Fundamentals - Variables & Type Casting

Demonstrating explicit type hinting, variable naming conventions,
and safe primitive casting common when parsing raw string data inputs.
"""

# Type Hints
raw_record_id: int = 10452
source_api_name: str = "dummy_json_recipes"
ingestion_rate_limit: float = 25.5
is_pipeline_active: bool = True

print(
    f"System Log: Ingesting from {source_api_name} "
    f"(ID: {raw_record_id})"
)

# Type Casting
raw_metric_string = "450"
processed_metric = int(raw_metric_string)

raw_price_string = "19.99"
processed_price = float(raw_price_string)

print(
    f"Type Transformation: "
    f"Converted '{raw_metric_string}' "
    f"to {type(processed_metric)}"
)

print(
    f"Type Transformation: "
    f"Converted '{raw_price_string}' "
    f"to {type(processed_price)}"
)