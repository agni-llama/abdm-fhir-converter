import uuid

from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.composition import CompositionSection
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.organization import Organization
from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.reference import Reference


def get_patient_construct(patient_info):
    name = patient_info["name"]
    gender = patient_info["gender"]
    patient_id = patient_info["patient_id"]
    abha_no = patient_info.get("abha_no")
    telephone_number = patient_info.get("telephone_number")

    identifier = [
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
            "value": patient_id,
        }
    ]

    if abha_no:
        identifier.append(
            {
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "AN",
                            "display": "Account number",
                        }
                    ]
                },
                "system": "https://healthid.ndhm.gov.in",
                "value": abha_no,
            }
        )
    extra_args = {}
    if telephone_number:
        extra_args["telecom"] = ContactPoint.construct(
            system="phone",
            value=telephone_number,
            use="mobile"
        )



    patient_ref_id = str(uuid.uuid4())
    patient_construct = Patient.construct(
        id=patient_ref_id,
        name=[{"text": name}],
        gender=gender,
        meta={"profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Patient"]},
        identifier=identifier,
        **extra_args
    )
    return patient_construct

def get_practitioner_construct(practitioner_info: dict):
    """
    :param practitioner_info:
    :return:
    """
    name = practitioner_info["name"]
    practitioner_id = practitioner_info["practitioner_id"]
    telephone_number = practitioner_info.get("telephone_number")

    extra_args = {}
    if telephone_number:
        extra_args["telecom"] = ContactPoint.construct(
            system="phone",
            value=telephone_number,
            use="mobile"
        )

    practitioner_ref_id = str(uuid.uuid4())
    practitioner_construct = Practitioner.construct(
        id=practitioner_ref_id,
        name=[{"text": name}],
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
                "value": practitioner_id,
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