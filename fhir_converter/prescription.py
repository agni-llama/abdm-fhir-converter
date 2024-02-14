import datetime
import uuid

from fhir.resources.bundle import Bundle, BundleEntry
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.composition import Composition
from fhir.resources.medicationrequest import MedicationRequest
from fhir.resources.reference import Reference

from fhir_converter.common import get_patient_construct, create_section, get_practitioner_construct


def create_prescription(input_json: dict):
    reference_data = []

    patient_info = input_json.get("patient", {})
    patient = get_patient_construct(patient_info)
    practitioner_info = input_json.get("practitioner", {})
    practitioner = get_practitioner_construct(practitioner_info)
    practitioner_ref = Reference.construct(
        reference=f"urn:uuid:/{practitioner.id}", display=practitioner.name[0]["text"]
    )
    patient_ref = Reference.construct(
        reference=f"urn:uuid:/{patient.id}", display=patient.name[0]["text"]
    )
    status = "final"
    resource_type = CodeableConcept.construct(
        text="Prescription record",
        coding=[
            Coding.construct(
                system="http://snomed.info/sct",
                code="440545006",
                display="Prescription record",
            )
        ],
    )
    prescription_date = input_json.get("prescription_date", datetime.datetime.now().isoformat())

    reference_data.append(patient)
    reference_data.append(practitioner)
    medication_requests = []

    medications = input_json.get("medications", [])
    for medication in medications:
        medication_request_id = str(uuid.uuid4())
        medication_request_construct = MedicationRequest.construct(
            id=medication_request_id,
            status="active",
            intent="order",
            medicationCodeableConcept=CodeableConcept.construct(
                text=medication.get("medication_name", "No Name")
            ),
            subject=patient_ref,
            authoredOn=prescription_date,
            requester=practitioner_ref,
            dosageInstruction=[
                {
                    "text": medication.get("dosage_instruction", "")
                }
            ]
        )
        medication_requests.append(medication_request_construct)
        reference_data.append(medication_request_construct)


    composition_id = str(uuid.uuid4())
    prescription = Composition.construct(
        id=composition_id,
        type=resource_type,
        title="Prescription record",
        date=prescription_date,
        status=status,
        subject=patient_ref,
        author=[practitioner_ref],
        section=[create_section(
            title="Prescription record",
            code="440545006",
            display="Prescription record",
            text="Prescription record",
            references=medication_requests,
        )]
    )

    bundle = Bundle.construct()
    bundle.type = "collection"
    bundle.entry = [
        BundleEntry.construct(
            fullUrl=f"urn:uuid:{composition_id}", resource=prescription
        ),
        BundleEntry.construct(fullUrl=f"urn:uuid:{patient.id}", resource=patient),
    ]
    for resource in reference_data:
        bundle.entry.append(
            BundleEntry.construct(fullUrl=f"urn:uuid:{resource.id}", resource=resource)
        )

    return bundle.json(indent=2)

if __name__ == "__main__":
    input_json = {
        "patient": {
            "name": "John Doe",
            "patient_id": "somepateintid"
        },
        "practitioner": {
            "name": "Dr. Smith",
            "practitioner_id": "somepractitionerid"
        },
        "prescription_date": "2021-10-10",
        "medications": [
            {
                "medication_name": "Aspirin",
                "dosage_instruction": "Take 1 tablet daily",
            },
            {
                "medication_name": "Aspirin 2",
                "dosage_instruction": "Take 2 tablet daily"
            }
        ]
    }
    print(create_prescription(input_json))