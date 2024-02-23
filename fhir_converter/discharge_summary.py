from typing import List
import uuid
from fhir.resources.bundle import Bundle
from fhir.resources.bundle import BundleEntry
from fhir.resources.coding import Coding

# from fhir.resources.coding import Coding
from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from fhir.resources.condition import Condition
from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.procedure import Procedure
from fhir.resources.composition import Composition
from fhir.resources.familymemberhistory import FamilyMemberHistory
from fhir.resources.familymemberhistory import FamilyMemberHistoryCondition
from fhir.resources.composition import CompositionSection
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.reference import Reference
import json

from fhir_converter.common import get_patient_construct, create_section

# from .utils import discharge_summary_section_details as section_details

section_details = {
    "chief_complaints": ("Chief Complaints", "422843007", "Chief complaint section"),
    "physical_examination": (
        "Physical Examination",
        "425044008",
        "Physical Examination section",
    ),
    "allergies": ("Allergies", "722446000", "Allergy record"),
    "medical_history": ("Medical History", "371529009", "History and physical report"),
    "family_history": ("Family History", "422432008", "Family history section"),
    "investigation_advice": ("Investigation Advice", "721963009", "Order document"),
    "medications": ("Medications", "721912009", "Medication summary document"),
    "follow_up": ("Follow Up", "390906007", "Follow-up encounter"),
    "procedure": ("Procedure", "371525003", "Procedure report"),
    "referral": ("Referral", "306206005", "Clinical procedure report"),
    "other_observations": ("Other Observations", "404684003", "Clinical finding"),
    "document_reference": (
        "Document Reference",
        "371530004",
        "Clinical consultation report",
    ),
}



def get_condition_construct(condition_info_text, subject):
    condition_id = str(uuid.uuid4())

    # TODO: apt snowmed code and descriptions to be extracted from the condition_info_text and added to the condition construct. below is a sample
    coding = [
        Coding.construct(
            system="http://snomed.info/sct",
            code="",
            display="",
        )
    ]

    condition_construct = Condition.construct(
        id=condition_id,
        code=CodeableConcept.construct(
            text=condition_info_text,
            coding=coding,
        ),
        text={
            "status": "generated",
            "div": f'<div xmlns="http://www.w3.org/1999/xhtml"><p>{condition_info_text}</p></div>',
        },
        subject=Reference.construct(reference=f"urn:uuid:/{subject.id}"),
    )
    return condition_construct


def get_observation_construct(observation_info_text, subject):
    observation_id = str(uuid.uuid4())

    coding = [
        Coding.construct(
            system="http://snomed.info/sct",
            code="",
            display="",
        )
    ]

    observation_construct = Observation.construct(
        id=observation_id,
        code=CodeableConcept.construct(
            text=observation_info_text,
            coding=coding,
        ),
        text={
            "status": "generated",
            "div": f'<div xmlns="http://www.w3.org/1999/xhtml"><p>{observation_info_text}</p></div>',
        },
        status="final",  # registered | preliminary | final | amended +
        subject=Reference.construct(reference=f"urn:uuid:{subject.id}"),
    )
    return observation_construct


def get_allergy_intolerance_construct(allergy_info_text, subject):
    allergy_id = str(uuid.uuid4())

    allergy_construct = AllergyIntolerance.construct(
        id=allergy_id,
        code=CodeableConcept.construct(
            text=allergy_info_text,
            coding=[
                Coding.construct(
                    system="http://snomed.info/sct",
                    code="",
                    display="",
                )
            ],
        ),
        text={
            "status": "generated",
            "div": f'<div xmlns="http://www.w3.org/1999/xhtml"><p>{allergy_info_text}</p></div>',
        },
        patient=Reference.construct(reference=f"urn:uuid:{subject.id}"),
    )
    return allergy_construct


def get_procedure_construct(procedure_info_text, subject):
    procedure_id = str(uuid.uuid4())

    procedure_construct = Procedure.construct(
        id=procedure_id,
        code=CodeableConcept.construct(
            text=procedure_info_text,
            coding=[
                Coding.construct(
                    system="http://snomed.info/sct",
                    code="",
                    display="",
                )
            ],
        ),
        text={
            "status": "generated",
            "div": f'<div xmlns="http://www.w3.org/1999/xhtml"><p>{procedure_info_text}</p></div>',
        },
        status="completed",  # preparation | in-progress | not-done | on-hold | stopped | completed | entered-in-error | unknown
        subject=Reference.construct(reference=f"urn:uuid:{subject.id}"),
    )
    return procedure_construct


def get_familymemberhistory_construct(familymemberhistory_info_text, subject):
    id = str(uuid.uuid4())

    familymemberhistory_construct = FamilyMemberHistory.construct(
        id=id,
        status="completed",  # partial | completed | entered-in-error | health-unknown
        patient=Reference.construct(reference=f"urn:uuid:{subject.id}"),
        relationship=CodeableConcept.construct(
            text=familymemberhistory_info_text,
            coding=[
                Coding.construct(
                    system="http://snomed.info/sct",
                    code="",
                    display="",
                )
            ],
        ),
        condition=[
            FamilyMemberHistoryCondition.construct(
                code=CodeableConcept.construct(
                    text=familymemberhistory_info_text,
                    coding=[
                        Coding.construct(
                            system="http://snomed.info/sct",
                            code="",
                            display="",
                        )
                    ],
                ),
                note=familymemberhistory_info_text,
            )
        ],
    )


def create_fhir_bundle_discharge_summary(input_json):
    patient_info = input_json.get("patient", {})
    meta_data = input_json.get("meta", {})
    input_section = input_json.get("section", {})

    patient = get_patient_construct(patient_info)

    section_config = {}

    # chief complaints section
    if input_section.get("chief_complaints"):
        chief_complaints = get_condition_construct(
            input_section.get("chief_complaints", ""), patient
        )
        section_config["chief_complaints"] = [chief_complaints]

    # physical examination section
    if input_section.get("physical_examination"):
        physical_examination = get_condition_construct(
            input_section.get("physical_examination", ""), patient
        )
        section_config["physical_examination"] = [physical_examination]

    # final composition
    composition_id = str(uuid.uuid4())
    composition = Composition.construct(
        id=composition_id,
        title="Discharge Summary",
        date=meta_data.get("discharge_date", ""),
        status=meta_data.get(
            "status", ""
        ),  # final | amended | entered-in-error | preliminary,
        type=CodeableConcept.construct(
            text="Discharge Summary",
            coding=[
                Coding.construct(
                    system="http://snomed.info/sct",
                    code="371530004",
                    display="Clinical consultation report",
                )
            ],
        ),
        subject=Reference.construct(
            reference=f"urn:uuid:{patient.id}", display=patient.name[0]["text"]
        ),
        section=[
            create_section(
                *section_details.get(title),
                input_json.get(title),
                section_config.get(title),
            )
            for title in section_config
        ],
    )

    unique_resources = []
    unique_resources_id = set()

    section_resources = section_config.items()
    for _, resources in section_resources:
        for resource in resources:
            if resource.id not in unique_resources_id:
                unique_resources.append(resource)
                unique_resources_id.add(resource.id)

    bundle = Bundle.construct()
    bundle.type = "collection"
    bundle.entry = [
        BundleEntry.construct(
            fullUrl=f"urn:uuid:{composition_id}", resource=composition
        ),
        BundleEntry.construct(fullUrl=f"urn:uuid:{patient.id}", resource=patient),
    ]
    for resource in unique_resources:
        bundle.entry.append(
            BundleEntry.construct(fullUrl=f"urn:uuid:{resource.id}", resource=resource)
        )

    return bundle.json(indent=2)


if __name__ == "__main__":
    print("FHIR Bundle for Discharge Summary")

    input_json = {
        "patient": {
            "patient_id": "1234567890",
            "name": "Aman",  # mandatory
            "gender": "Male",  # mandatory
            "base64_file": "sample text",
            "dob": "sample text",
            "phone": "sample text",
        },
        "section": {
            "chief_complaints": "sample text",
            "physical_examination": "sample text",
            "allergies": None,
            "medical_history": None,
            "family_history": None,
            "investigation_advice": None,
            "medications": None,
            "follow_up": None,
            "procedure": None,
            "referral": None,
            "other_observations": None,
            "document_reference": None,
        },
        "meta": {
            "discharge_date": "2020-07-09T15:32:26.605+05:30",
            "status": "final",  # final | amended | entered-in-error | preliminary
        },
    }

    fhir_bundle = create_fhir_bundle_discharge_summary(input_json)
    print(fhir_bundle)
