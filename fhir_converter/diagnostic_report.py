import datetime
import uuid
from pydantic.v1 import Field
from fhir.resources import datatype
from fhir.resources.R4B.diagnosticreport import DiagnosticReport
from fhir.resources.R4B.media import Media
from fhir.resources.R4B.servicerequest import ServiceRequest
from fhir.resources.attachment import Attachment
from fhir.resources.backboneelement import BackboneElement
from fhir.resources.bundle import Bundle, BundleEntry
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.composition import Composition
from fhir.resources.medicationrequest import MedicationRequest
from fhir.resources.observation import Observation
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference

from fhir_converter.common import get_patient_construct, create_section, get_practitioner_construct, \
    get_organization_construct


class MediaType(datatype.DataType):

    resource_type = Field("MediaType", const=True)

    link: Reference = Field(
        None,
        alias="link",
        title="Link of media",
        description="media link",
        # if property is element of this resource.
        element_property=True,
    )

    @classmethod
    def elements_sequence(cls):
        """returning all elements names from
        ``MediaType`` according specification,
        with preserving original sequence order.
        """
        return ["link"]

def create_diagnostic_report(input_json: dict):
    reference_data = []

    patient_info = input_json.get("patient", {})
    patient = get_patient_construct(patient_info)
    practitioner_info = input_json.get("practitioner", {})
    practitioner = get_practitioner_construct(practitioner_info)
    performer_info = input_json.get("performer", {})
    performer = get_organization_construct(performer_info)
    performer_ref = Reference.construct(
        reference=f"urn:uuid:{performer.id}", display=performer.name[0]["text"]
    )
    practitioner_ref = Reference.construct(
        reference=f"urn:uuid:{practitioner.id}", display=practitioner.name[0]["text"]
    )
    patient_ref = Reference.construct(
        reference=f"urn:uuid:{patient.id}", display=patient.name[0]["text"]
    )
    service_request = ServiceRequest.construct(
        id=str(uuid.uuid4()),
        status="active",
        intent="original-order",
        code=CodeableConcept.construct(
            text=input_json.get("request").get("service_name", "No Name")
        ),
        requester=practitioner_ref,
        subject=patient_ref,
        occurrenceDateTime=input_json.get("request").get("request_date")
    )
    service_request_ref = Reference.construct(
        reference=f"urn:uuid:/{service_request.id}", display=f"ServiceRequest/{service_request.code.text}"
    )

    status = "final"
    resource_type = CodeableConcept.construct(
        text="Diagnostic Report- Lab",
        coding=[
            Coding.construct(
                system="http://snomed.info/sct",
                code="721981007",
                display="Diagnostic studies report",
            )
        ],
    )
    report_date = input_json.get("report_date")

    reference_data.append(patient)
    reference_data.append(practitioner)
    reference_data.append(performer)
    reference_data.append(service_request)

    report_title = input_json.get("report_title")

    observations = []
    observation_reports = input_json.get("observations", [])
    for observation in observation_reports:
        request_id = str(uuid.uuid4())
        observation_construct = Observation.construct(
            id=request_id,
            status="final",
            code=CodeableConcept.construct(
                text=observation.get("observation_name")
            ),
            subject=patient_ref,
            issued=report_date,
            performer=performer_ref,
            valueQuantity=Quantity.construct(
                value=observation.get("observation_value"),
                unit=observation.get("observation_unit")
            ),
            referenceRange=[{
                "low": {
                    "value": observation.get("ref_low"),
                    "unit": observation.get("observation_unit")
                },
                "high": {
                    "value": observation.get("ref_high"),
                    "unit": observation.get("observation_unit")
                }
            }]
        )
        observations.append(observation_construct)
        reference_data.append(observation_construct)

    request_id = str(uuid.uuid4())
    if input_json.get("imaging"):
        link_media = Media.construct(
            id=str(uuid.uuid4()),
            status="completed",
            content=Attachment.construct(
                contentType=input_json["imaging"]["type"],
                data=input_json["imaging"]["data"]
            )
        )
        reference_data.append(link_media)
        link_media_ref = Reference.construct(
            reference=f"urn:uuid:{link_media.id}", display="Imaging data"
        )

        diagnostic_report_construct = DiagnosticReport.construct(
            id=request_id,
            status="final",
            code=CodeableConcept.construct(
                text=input_json.get("report_name")
            ),
            subject=patient_ref,
            issued=report_date,
            performer=performer_ref,
            media = [
                MediaType.construct(
                    link=link_media_ref
                )
            ]
        )
    else:
        diagnostic_report_construct = DiagnosticReport.construct(
            id=request_id,
            status="active",
            intent="order",
            basedOn=[service_request_ref],
            code=CodeableConcept.construct(
                text=input_json.get("report_name")
            ),
            subject=patient_ref,
            issued=report_date,
            requester=practitioner_ref,
            performer=performer_ref,
            results_interpretation=[practitioner_ref],
            results=[Reference.construct(
                reference=f"urn:uuid:/{observation.id}", display=f"Observation/{observation.code.text}"
            ) for observation in observations],
            conclusion=input_json.get("conclusion", "No Conclusion")
        )
    reference_data.append(diagnostic_report_construct)

    composition_id = str(uuid.uuid4())
    prescription = Composition.construct(
        id=composition_id,
        type=resource_type,
        title="Diagnostic Report",
        date=report_date,
        status=status,
        subject=patient_ref,
        author=[practitioner_ref],
        section=[create_section(
            title=report_title,
            code="",
            display="",
            text="",
            references=[diagnostic_report_construct],
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
            "patient_id": "somepateintid",
            "gender": "Male"
        },
        "practitioner": {
            "name": "Dr. Smith",
            "practitioner_id": "somepractitionerid",
            "gender": "Male"
        },
        "performer": {
            "name": "Org XYZ Ltd.",
            "organization_id": "Org XYZ Ltd. ID"
        },
        "report_date": "2021-10-10",
        "request":{
            "service_name": "Blood Test",
            "request_date": "2021-10-10"
        },
        "report_name": "Blood Test Report",
        "report_title": "BloodTest",
        "conclusion": "Normal",
        "observations": [
            {
                "observation_name": "RBC",
                "observation_value": "100",
                "observation_unit": "mg/dL",
                "ref_low": "50",
                "ref_high": "150"
            },
            {
                "observation_name": "WBC",
                "observation_value": "100",
                "observation_unit": "mg/dL",
                "ref_low": "60",
                "ref_high": "160"
            }
        ],
        "imaging": {
            "type": "image/jpeg",
            "data": "base64 encoded data"
        }
    }
    print(create_diagnostic_report(input_json))