import json
import random
from faker import Faker

# Initialize Faker
fake = Faker()

# Predefined lists of medical data
conditions_list = ["Diabetes", "Hypertension", "Asthma", "COPD", "Chronic Kidney Disease", "Anemia", "Hyperlipidemia"]
medications_list = ["Metformin 500mg", "Losartan 50mg", "Atorvastatin 10mg", "Salbutamol Inhaler", "Lisinopril 20mg"]
allergies_list = ["Penicillin", "Peanuts", "Lactose", "Dust", "Shellfish"]
lab_tests = ["Blood Sugar", "Cholesterol", "Hemoglobin", "Creatinine", "Liver Enzymes"]


# Function to generate synthetic patient records
def generate_synthetic_ehr(num_records=10):
    patients = []

    for _ in range(num_records):
        patient = {
            "patient_id": fake.uuid4(),
            "name": fake.name(),
            "age": random.randint(25, 80),
            "gender": random.choice(["Male", "Female", "Other"]),
            "conditions": random.sample(conditions_list, k=random.randint(1, 3)),
            "medications": random.sample(medications_list, k=random.randint(1, 3)),
            "allergies": random.sample(allergies_list, k=random.randint(0, 2)),
            "lab_results": {test: f"{random.randint(50, 250)} mg/dL" for test in random.sample(lab_tests, k=2)},
            "visit_history": [
                {"date": fake.date_this_decade().strftime("%Y-%m-%d"), "doctor_notes": fake.sentence()}
                for _ in range(random.randint(1, 3))
            ]
        }
        patients.append(patient)

    return patients


# Generate EHR data
num_records = 10  # Change this value as needed
ehr_data = generate_synthetic_ehr(num_records)

# Save to JSON file
with open("synthetic_ehr_data.json", "w") as f:
    json.dump(ehr_data, f, indent=4)

print(f"✅ Successfully generated {num_records} synthetic EHR records and saved to 'synthetic_ehr_data.json'.")
