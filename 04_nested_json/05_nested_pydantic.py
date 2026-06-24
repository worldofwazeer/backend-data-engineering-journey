"""
04_Nested_JSON - Nested Pydantic Models
Leveraging composed sub-models to strictly validate multi-layered payloads.
"""
from pydantic import BaseModel, ValidationError

class ConnectionSettings(BaseModel):
    host: str
    port: int

class ServiceConfiguration(BaseModel):
    service_name: str
    connection: ConnectionSettings # Referencing another model schema directly

valid_json_input = {
    "service_name": "Scraper_Engine",
    "connection": {"host": "127.0.0.1", "port": 9000}
}

try:
    config = ServiceConfiguration(**valid_json_input)
    print(f"Complex Validation Cleared: {config.service_name} bound to port {config.connection.port}")
except ValidationError as e:
    print(f"Nested Validation Failed:\n{e}")