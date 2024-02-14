import uuid

from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.composition import CompositionSection
from fhir.resources.organization import Organization
from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.reference import Reference


def get_patient_construct(patient_info):
    patient_id = str(uuid.uuid4())
    patient_construct = Patient.construct(
        id=patient_id,
        name=[{"text": patient_info.get("name", "No Name")}],
        gender=patient_info.get("gender", ""),
        meta={"profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Patient"]},
        identifier=[
            {
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "MR",
                            "display": "Medical record number",
                        }
                    ]
                },
                "system": "https://healthid.ndhm.gov.in",
                "value": patient_info.get("patient_id", "1234567890"),
            }
        ],
    )
    return patient_construct

def get_practitioner_construct(practitioner_info: dict):
    """
    :param practitioner_info:
    :return:
    """
    practitioner_id = str(uuid.uuid4())
    practitioner_construct = Practitioner.construct(
        id=practitioner_id,
        name=[{"text": practitioner_info.get("name", "No Name")}],
        meta={"profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Practitioner"]},
        identifier=[
            {
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "PRN",
                            "display": "Provider number",
                        }
                    ]
                },
                "system": "https://healthid.ndhm.gov.in",
                "value": practitioner_info.get("practitioner_id", "1234567890"),
            }
        ],
    )
    return practitioner_construct

def get_organization_construct(organization_info: dict):
    """
    :param practitioner_info:
    :return:
    """
    organization_id = str(uuid.uuid4())
    organization_construct = Organization.construct(
        id=organization_id,
        name=[{"text": organization_info.get("name", "No Name")}],
        meta={"profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Practitioner"]},
        identifier=[
            {
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "PRN",
                            "display": "Provider number",
                        }
                    ]
                },
                "system": "https://facility.ndhm.gov.in",
                "value": organization_info.get("organization_id", "1234567890"),
            }
        ],
    )
    return organization_construct

def create_section(title, code, display, text, references):
    section = CompositionSection.construct(
        title=title,
        code=CodeableConcept.construct(
            text=text,
            coding=[
                Coding.construct(
                    system="http://snomed.info/sct", code=code, display=display
                )
            ],
        ),
        text=text,
        entry=[
            Reference.construct(reference=f"urn:uuid:{ref.id}")
            for ref in references
            if ref
        ],
    )
    return section