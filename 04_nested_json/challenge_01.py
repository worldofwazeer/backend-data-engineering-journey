import logging
from typing import Any
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from pydantic.alias_generators import to_camel

# SETUP: LOGGING
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("etl_pipeline")


class BaseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ContactInfo(BaseSchema):
    phone: str = Field(min_length=1)
    email: EmailStr | None = None


class MedicalHistory(BaseSchema):
    blood_type: str = Field(min_length=1)
    allergies: list[str] | None = None


class PatientRecord(BaseSchema):
    id: int = Field(gt=0)
    patient_name: str = Field(min_length=1)
    contact_info: ContactInfo

    medical_history: MedicalHistory | None = None


def flatten_patient(patient: PatientRecord) -> dict[str, Any]:
    flat_row = {
        "patient_id": patient.id,
        "patient_name": patient.patient_name,
        "phone_number": patient.contact_info.phone,
    }

    # STEP 2: Safe Extraction for Email
    if patient.contact_info.email:
        flat_row["email"] = str(patient.contact_info.email)
    else:
        flat_row["email"] = "No Email"

    # STEP 3: Safe Extraction for the Medical Dictionary
    if patient.medical_history:
        # If the dictionary exists, grab the blood type
        flat_row["blood_type"] = patient.medical_history.blood_type

        # Check if they have allergies inside that dictionary
        if patient.medical_history.allergies:
            flat_row["allergies"] = ", ".join(patient.medical_history.allergies)
        else:
            flat_row["allergies"] = "None"

    else:
        # If the ENTIRE medical history dictionary is None (like Patient 2)
        flat_row["blood_type"] = "Unknown"
        flat_row["allergies"] = "None"

    # STEP 4: Return the finished row at the VERY END
    return flat_row