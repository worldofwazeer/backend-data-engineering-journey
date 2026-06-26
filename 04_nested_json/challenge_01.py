"""
Challenge 01 - Automated Patient Data Flattening & Schema Validation Ingestion
"""
import logging
from typing import Any, List, Dict
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from pydantic.alias_generators import to_camel

# SETUP: LOGGING TELEMETRY
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger("patient_etl")


class BaseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ContactInfo(BaseSchema):
    phone: str = Field(min_length=1)
    email: EmailStr | None = None


class MedicalHistory(BaseSchema):
    blood_type: str = Field(min_length=1)
    allergies: List[str] | None = None


class PatientRecord(BaseSchema):
    id: int = Field(gt=0)
    patient_name: str = Field(min_length=1)
    contact_info: ContactInfo
    medical_history: MedicalHistory | None = None


def flatten_patient(patient: PatientRecord) -> Dict[str, Any]:
    """
    Transforms a deeply nested Pydantic PatientRecord into a clean, 
    flat dictionary optimized for relational database ingestion.
    """
    medical = patient.medical_history
    contact = patient.contact_info

    # Clean, concise, and Pythonic dict building using inline ternary expressions
    return {
        "patient_id": patient.id,
        "patient_name": patient.patient_name,
        "phone_number": contact.phone,
        "email": str(contact.email) if contact.email else "No Email",
        "blood_type": medical.blood_type if medical else "Unknown",
        "allergies": ", ".join(medical.allergies) if medical and medical.allergies else "None"
    }


def run_ingestion_pipeline(raw_payloads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Validates incoming raw records against schema constraints and flattens them.
    """
    logger.info(f"Starting Ingestion Cycle: Processing {len(raw_payloads)} incoming payload strings.")
    flattened_records: List[Dict[str, Any]] = []

    for idx, raw_data in enumerate(raw_payloads, start=1):
        try:
            # Validate raw JSON-like dictionary into strong Pydantic objects
            patient_obj = PatientRecord.model_validate(raw_data)

            # Flatten the object
            flat_data = flatten_patient(patient_obj)
            flattened_records.append(flat_data)

            logger.info(f"Record {idx}/{len(raw_payloads)} parsed successfully. ID: {flat_data['patient_id']}")

        except Exception as e:
            logger.error(f"Schema violation detected on Record Index {idx}! Validation Error: {e}")
            continue

    logger.info(f"Ingestion Cycle Finished. Successfully normalized {len(flattened_records)} rows.")
    return flattened_records


if __name__ == "__main__":
    # Simulated incoming API response data using camelCase properties
    mock_api_payload = [
        {
            "id": 101,
            "patientName": "Alhaji Ibrahim",
            "contactInfo": {
                "phone": "+2348012345678",
                "email": "ibrahim@example.com"
            },
            "medicalHistory": {
                "bloodType": "O+",
                "allergies": ["Dust", "Penicillin"]
            }
        },
        {
            "id": 102,
            "patientName": "Musa Garba",
            "contactInfo": {
                "phone": "+2348098765432",
                "email": None
            },
            "medicalHistory": None  # Edge case: Missing entire medical object
        },
        {
            "id": -5,  # Data Anomaly: Invalid ID boundary rule (id must be gt 0)
            "patientName": "Malfunctioning Row Record",
            "contactInfo": {
                "phone": "",
                "email": "malformed-email"
            }
        }
    ]

    print("\n--- RUNNING INGESTION LIVE TEST ---\n")
    processed_dataset = run_ingestion_pipeline(mock_api_payload)
    print("\n--- FINAL OUTBOUND DATA ASSET ---")
    print(processed_dataset)