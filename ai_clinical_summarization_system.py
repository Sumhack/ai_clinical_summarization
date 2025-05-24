import gradio as gr
import json
from faster_whisper import WhisperModel
import google.generativeai as genai
from pymongo import MongoClient

# Configure Gemini API
genai.configure(api_key=<api_key>)
models = genai.GenerativeModel("gemini-1.5-flash")

# MongoDB connection
uri = <mongodb_uri>
client = MongoClient(uri)
db = client["ehr_database"]
patients_collection = db["patients"]

# Load Whisper model
model = WhisperModel("small")

def get_patient_list():
    """Fetch patient names and IDs from MongoDB."""
    patients = patients_collection.find({}, {"_id": 0, "patient_id": 1, "name": 1})
    return {patient["name"]: patient["patient_id"] for patient in patients}

def generate_summary(conversation_text, patient_history=None):
    """Generate AI-based summaries."""
    prompt_plain = f"Summarize the following doctor-patient conversation:\n{conversation_text}"
    responses = models.generate_content(prompt_plain)
    plain_summary = responses.text

    if patient_history:
        prompt_medical = f"""
        Given the patient's medical history:
        {json.dumps(patient_history, indent=2)}

        And the following doctor-patient conversation:
        {conversation_text}

        Generate a medically relevant summary.
        """
        response_medical = models.generate_content(prompt_medical)
        medical_summary = response_medical.text
    else:
        medical_summary = "No medical history available."

    return plain_summary, medical_summary

def transcribe_audio(patient_name, audio_file):
    """Transcribe audio and generate summaries."""
    patient_id = patient_dict.get(patient_name)
    if not patient_id:
        return "Patient not found", "", ""

    patient = patients_collection.find_one({"patient_id": patient_id}, {"_id": 0})
    if not patient:
        return "Patient data not found", "", ""

    segments, _ = model.transcribe(audio_file)
    transcription = " ".join([s.text for s in segments])

    plain_summary, medical_summary = generate_summary(transcription, patient)

    return transcription, plain_summary, medical_summary

# Fetch patient list
patient_dict = get_patient_list()
patient_names = list(patient_dict.keys())

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("## Doctor-Patient Conversation Analysis")

    with gr.Row():
        patient_dropdown = gr.Dropdown(choices=patient_names, label="Select Patient")
        audio_input = gr.Audio(sources=["upload"], type="filepath", label="Upload Audio")

    transcribe_button = gr.Button("Transcribe & Summarize")

    with gr.Row():
        transcription_output = gr.Textbox(label="Transcription", interactive=False)

    with gr.Row():
        plain_summary_output = gr.Textbox(label="General Summary", interactive=False)
        medical_summary_output = gr.Textbox(label="Medical Summary", interactive=False)

    transcribe_button.click(transcribe_audio, inputs=[patient_dropdown, audio_input],
                            outputs=[transcription_output, plain_summary_output, medical_summary_output])

# Launch the app
demo.launch(debug=True)
