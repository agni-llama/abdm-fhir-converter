import uuid

from fhir.resources.bundle import Bundle
from fhir.resources.bundle import BundleEntry
from fhir.resources.coding import Coding
from fhir.resources.composition import Composition
from fhir.resources.composition import CompositionSection
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.reference import Reference

from fhir_converter.common import get_patient_construct, get_practitioner_construct


def create_section(title, code, display, text):
    ref_id = str(uuid.uuid4())
    section = CompositionSection.construct(
        id=ref_id,
        title=title,
        code=CodeableConcept.construct(
            text=display,
            coding=Coding.construct(
                system="http://snomed.info/sct",
                code=code,
                display=display
            )
        ),
        text=text
    )
    return section


def create_opconsult_record(input_json):
    patient_info = input_json.get("patient", {})

    patient = get_patient_construct(patient_info)
    patient_ref = Reference.construct(
        reference=f"urn:uuid:{patient.id}", display=patient.name[0]["text"]
    )

    practitioner_info = input_json.get("practitioner", {})
    practitioner = get_practitioner_construct(practitioner_info)
    practitioner_ref = Reference.construct(
        reference=f"urn:uuid:{practitioner.id}", display=practitioner.name[0]["text"]
    )

    ref_data = [patient, practitioner]

    section_details = {
        "Chief Complaints": ("422843007", "Chief complaint section"),
        "Physical Examination": ("422843007", "Physical Examination section"),
        "Allergies": ("722446000", "Allergy record"),
        "Medical History": ("371529009", "History and physical report"),
        "Family History": ("422432008", "Family history section"),
        "Investigation Advice": ("721963009", "Order document"),
        "Medications": ("721912009", "Medication summary document"),
        "Follow Up": ("390906007", "Follow-up encounter"),
        "Procedure": ("371525003", "Procedure report"),
        "Referral": ("306206005", "Clinical procedure report"),
        "Other Observations": ("404684003", "Clinical finding"),
        "Document Reference": ("371530004", "Clinical consultation report"),
    }

    sections = [
        create_section(title, *details, input_json.get(title.replace(" ", ""), "")) for title, details in
        section_details.items()
    ]

    ref_data.extend(sections)

    section_refs = [Reference.construct(reference=f"urn:uuid:{section.id}") for section in sections]

    # Create Composition resource for OP Consult Record
    composition = Composition.construct(
        title="OP Consult Record",
        date=input_json["date"],
        status="final",  # final | amended | entered-in-error | preliminary,
        type=CodeableConcept.construct(
            text="OP Consult Record",
            coding=Coding.construct(
                system="http://snomed.info/sct",
                code="371530004",
                display="Clinical consultation report"
            )
        ),
        author=[practitioner_ref],
        subject=patient_ref,
        section=section_refs
    )

    bundle = Bundle.construct()
    bundle.type = "collection"
    bundle.entry = [
        BundleEntry.construct(resource=composition)
    ]
    bundle.entry.extend(ref_data)

    return bundle.json(indent=2)

if __name__ == "__main__":
    print("FHIR Bundle for OP Consult Record")
    input_json = {
        "patient": {
            "name": "Aman",
            "gender": "Male",
            "patient_id": "1234567890",
            "telecom": "1234567890",
        },
        "practitioner": {
            "name": "Aman Practitioner",
            "gender": "Female",
            "practitioner_id": "1234567890",
            "telecom": "1234567890",
        },
        "date": "2021-06-01",
        "ChiefComplaints": "sample text",
        "PhysicalExamination": "sample text",
        "Allergies": "sample text",
        "MedicalHistory": "sample text",
        "FamilyHistory": "sample text",
        "InvestigationAdvice": "sample text",
        "Medications": "sample text",
        "FollowUp": "sample text",
        "Procedure": "sample text",
        "Referral": "sample text",
        "OtherObservations": "sample text",
        "DocumentReference": "sample text",
    }

    fhir_bundle = create_opconsult_record(input_json)
    print(fhir_bundle)
