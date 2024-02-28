# ABDM-Compliant FHIR Converter

## Introduction
This project provides a FHIR (Fast Healthcare Interoperability Resources) converter compliant with the Ayushman Bharat Digital Mission (ABDM) standards, as outlined by the National Resource Centre for EHR Standards ([NRCeS](https://nrces.in/)) in India. It aims to facilitate the seamless conversion of healthcare data into FHIR-compliant formats, ensuring interoperability and accessibility across different healthcare systems in India.

For more information on ABDM FHIR profiles, visit the [ABDM FHIR Implementation Guide](https://nrces.in/ndhm/fhir/r4/profiles.html).


## Features
- **Compliance with ABDM**: Adheres to the FHIR profiles and standards specified for the ABDM ecosystem.
- **Wide Coverage**: Supports a broad range of healthcare data types, including patient records, clinical notes, lab reports, etc.

## Installation

```bash
pip install git+https://github.com/agni-llama/fhir-converter   
```

## Usage Examples

### Discharge Summary Conversion

```
from fhir_converter import create_fhir_bundle_discharge_summary
input_json = {
  "patient": {
    "patient_id": "1234567890",
    "name": "Aman",
    "gender": "Male",
    "base64_file": "dGhpcyBpcyBhIHNhbXBsZSBiYXNlNjQgZW5jb2RlZCBmaWxl",
    "dob": "1990-01-01",
    "phone": "+911234567890"
  },
  "section": {
    "chief_complaints": "Persistent cough and fever for the past 7 days.",
    "physical_examination": "Temperature of 38.5°C, Normal breathing sounds.",
    "allergies": "No known allergies.",
    "medical_history": "Diagnosed with asthma in 2010.",
    "family_history": "Father has a history of hypertension.",
    "investigation_advice": "Recommended chest X-ray and blood tests.",
    "medications": "Paracetamol 500mg, twice a day for 5 days.",
    "follow_up": "Follow-up visit scheduled in 1 week.",
    "procedure": "Nebulization with Salbutamol.",
    "referral": "Referred to a pulmonologist for further evaluation.",
    "other_observations": "Patient advised to maintain hydration and rest.",
    "document_reference": "Refer to attached chest X-ray report."
  },
  "meta": {
    "discharge_date": "2020-07-09T15:32:26.605+05:30",
    "status": "final"
  }
}

discharge_fhir_bundle = create_fhir_bundle_discharge_summary(input_json)
print(discharge_fhir_bundle)
```

### OPConsult Record Conversion


```
from fhir_converter import create_opconsult_record
input_json = {
    "patient": {
        "name": "Aman Kumar",
        "gender": "Male",
        "patient_id": "P123456789",
        "telecom": "+911234567890",
    },
    "practitioner": {
        "name": "Dr. Anita Desai",
        "gender": "Female",
        "practitioner_id": "PR987654321",
        "telecom": "+919876543210",
    },
    "date": "2023-01-15",
    "ChiefComplaints": "Persistent cough and fever for 5 days",
    "PhysicalExamination": "Temperature of 38.5°C, clear lungs on auscultation",
    "Allergies": "No known allergies",
    "MedicalHistory": "Diagnosed with asthma in childhood",
    "FamilyHistory": "Mother has a history of hypertension",
    "InvestigationAdvice": "Complete blood count, Chest X-ray",
    "Medications": "Paracetamol 500mg every 8 hours for 5 days",
    "FollowUp": "Return in one week or sooner if symptoms worsen",
    "Procedure": "Nebulization with salbutamol",
    "Referral": "Consult with a pulmonologist if no improvement",
    "OtherObservations": "Patient is a non-smoker",
    "DocumentReference": "Refer to attached X-ray report",
}
print(create_opconsult_record(input_json))

```

### Prescription Record Conversion


```
from fhir_converter import create_prescription
input_json = {
  "patient": {
    "name": "John Doe",
    "patient_id": "somepatientid"
  },
  "practitioner": {
    "name": "Dr. Smith",
    "practitioner_id": "somepractitionerid"
  },
  "prescription_date": "2021-10-10",
  "medications": [
    {
      "medication_name": "Aspirin",
      "dosage_instruction": "Take 1 tablet daily with food."
    },
    {
      "medication_name": "Metformin",
      "dosage_instruction": "Take 500 mg twice a day before meals."
    }
  ]
}

prescription_fhir_bundle = create_prescription(input_json)
print(prescription_fhir_bundle)

```

### Diagnostic Report Conversion


```
from fhir_converter import create_fhir_diagnostic_report
input_json = {
    "patient": {
        "name": "Rahul Mehra",
        "patient_id": "P987654321",
        "gender": "male"
    },
    "practitioner": {
        "name": "Dr. Rakesh Sharma",
        "practitioner_id": "PR123456789",
        "gender": "male"
    },
    "performer": {
        "name": "Path Labs Pvt. Ltd.",
        "organization_id": "PL98765"
    },
    "report_date": "2023-02-20",
    "request":{
        "service_name": "Comprehensive Metabolic Panel",
        "request_date": "2023-02-18"
    },
    "report_name": "Comprehensive Metabolic Panel Report",
    "report_title": "CMP",
    "conclusion": "Liver function tests within normal limits, elevated glucose levels suggesting possible glucose intolerance.",
    "observations": [
        {
            "observation_name": "Glucose",
            "observation_value": "120",
            "observation_unit": "mg/dL",
            "ref_low": "70",
            "ref_high": "100"
        },
        {
            "observation_name": "ALT",
            "observation_value": "30",
            "observation_unit": "U/L",
            "ref_low": "7",
            "ref_high": "56"
        }
    ],
    "imaging": {
        "type": "image/jpeg",
        "data": "base64_encoded_data_of_an_X-ray"
    }
}
diagnostic_fhir_bundle = create_fhir_diagnostic_report(input_json)
print(diagnostic_fhir_bundle)
```


