from gtts import gTTS
import json
import os
from pydub import AudioSegment
from pydub.playback import play

# Load generated conversation
with open("generated_conversation.json", "r") as f:
    data = f.read()
    #print(f"File Content: {data}")
    #print(type(data))

    try:
        conversation = json.loads(data)  # Proper JSON parsing
        print("✅ JSON Loaded Successfully!")
    except json.JSONDecodeError as e:
        print(f"❌ JSON Error: {e}")


lines = conversation["transcribed_text"].split("\n\n")  # Split by dialogue blocks

# Define voice settings
doctor_voice = "en-uk"  # British accent for doctor
patient_voice = "en-au"  # American accent for patient

audio_clips = []

# Process each line separately
for line in lines:
    if line.startswith("Doctor:"):
        text = line.replace("Doctor: ", "")
        tts = gTTS(text=text, lang=doctor_voice)
        filename = f"doctor_{len(audio_clips)}.mp3"
    elif line.startswith("Patient:"):
        text = line.replace("Patient: ", "")
        tts = gTTS(text=text, lang=patient_voice)
        filename = f"patient_{len(audio_clips)}.mp3"
    else:
        continue  # Skip invalid lines

    # Save and load audio
    tts.save(filename)
    audio_clips.append(AudioSegment.from_file(filename, format="mp3"))

# Merge all audio clips into one
final_audio = sum(audio_clips)

# Save final conversation audio
final_audio.export("Andrew_conversation_audio.mp3", format="mp3")

# Play the final audio (optional)
play(final_audio)

print("✅ Conversation audio generated and saved as 'conversation_audio.mp3'!")
