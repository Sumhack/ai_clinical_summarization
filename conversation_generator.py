#import google.generativeai as genai
import json
#import random
import google.generativeai as genai

# Configure Gemini API Key
genai.configure(api_key=<google_api_key>)
model = genai.GenerativeModel("gemini-1.5-flash")

# Sample patient data (You can replace this with MongoDB queries)
patient_data = {
        "patient_id": "c326f4bc-a4c1-48e8-a83d-f6d986019f7f",
        "name": "Andrew Harrison",
        "age": 29,
        "gender": "Other",
        "conditions": [
            "Asthma"
        ],
        "medications": [
            "Salbutamol Inhaler",
            "Metformin 500mg",
            "Lisinopril 20mg"
        ],
        "allergies": [
            "Peanuts"
        ],
        "lab_results": {
            "Blood Sugar": "110 mg/dL",
            "Cholesterol": "146 mg/dL"
        },
        "visit_history": [
            {
                "date": "2021-09-13",
                "doctor_notes": "Purpose hard fly old professor seem who."
            },
            {
                "date": "2024-08-18",
                "doctor_notes": "Here response again cold well its."
            }
        ]
    }


# Function to generate conversation using Gemini LLM
def generate_conversation(patient):
    prompt = f"""
    Generate a detailed doctor-patient conversation based on the following medical history:

    Patient Name: {patient['name']}
    Age: {patient['age']}
    Gender: {patient['gender']}
    Conditions: {", ".join(patient['conditions'])}
    Medications: {", ".join(patient['medications'])}
    Allergies: {", ".join(patient['allergies']) if patient['allergies'] else "None"}
    Recent Lab Results: {json.dumps(patient['lab_results'])}
    Visit History: {json.dumps(patient['visit_history'])}

    The conversation should be **realistic** and include:
    - The doctor asking about symptoms related to the patient's conditions.
    - The patient responding with detailed complaints or improvements.
    - The doctor referencing past visit notes and suggesting next steps.

    Format the output in this structured JSON:
    {{
        "doctor": "Dr. Neil Starc",
        "patient": "{patient['name']}",
        "age": {patient['age']},
        "chief_complaint": "...",
        "transcribed_text": "Doctor: ... Patient: ... Doctor: ..."
    }}
    """

    response = model.generate_content(prompt)
    #print(response.text)

    return response.text  # Gemini may return text instead of JSON, so handle it accordingly


# Generate conversation
conversation = generate_conversation(patient_data)

# Save to a file
with open("generated_conversation.json", "w") as f:
    f.write(conversation)

print("✅ Conversation generated and saved!")
