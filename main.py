import streamlit as st
import sounddevice as sd
import wavio
import os
import google.generativeai as palm
import pathlib

# Constants
RECORDING_FILE = "test.mp3"
GEMINI_API_KEY = "Enter Key"

# Initialize Palm (Gemini 1.5) client
palm.configure(api_key=GEMINI_API_KEY)
model = palm.GenerativeModel(model_name="gemini-1.5-flash")

# Initialize session state for recording status and latest interaction
if 'is_recording' not in st.session_state:
    st.session_state['is_recording'] = False
if 'latest_interaction' not in st.session_state:
    st.session_state['latest_interaction'] = {"user": "", "ai": ""}

# Function to record audio
def record_audio(duration=5, sample_rate=44100):
    st.write(f"🎤 Recording for {duration} seconds...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Wait for the recording to finish
    wavio.write(RECORDING_FILE, recording, sample_rate, sampwidth=2)
    st.session_state['is_recording'] = False  # Automatically stop recording
    st.success("✅ Recording complete!")
    process_audio(RECORDING_FILE)  # Automatically process the recording immediately

# Function to stop recording
def stop_recording():
    if st.session_state['is_recording']:
        sd.stop()
        st.session_state['is_recording'] = False
        st.success("⏹️ Recording stopped!")
        process_audio(RECORDING_FILE)

# Transcribe the audio using Gemini
def transcribe_with_gemini(audio):
    st.write("📝 Transcribing the audio file with Gemini...")
    response = model.generate_content([
        "Please transcribe this recording:",
        {
            "mime_type": "audio/mp3",
            "data": pathlib.Path(audio).read_bytes()
        }
    ])
    if response:
        return response.text
    return None

# Get AI response to the transcription
def get_gemini_answer(transcript):
    st.write("🤖 Sending transcription to Gemini for a response...")
    try:
        # Handle user prompt for latest question
        if transcript.strip().lower() == "what was my last question":
            if st.session_state['latest_interaction']['user']:
                return f"Your last question was: '{st.session_state['latest_interaction']['user']}'"
            else:
                return "You haven't asked any questions yet."

        # Create a prompt with the transcript
        prompt = transcript
        response = model.generate_content(prompt)
        if response:
            return response.text
        else:
            st.error("❌ Gemini was unable to generate a response.")
            return "Sorry, Gemini was unable to generate a response."
    except Exception as e:
        st.error(f"❌ An error occurred while getting a response from Gemini: {e}")
        return "Sorry, an error occurred while getting a response from Gemini."

# Process the recorded audio
def process_audio(audio_file):
    if os.path.exists(audio_file):
        transcription = transcribe_with_gemini(audio_file)
        if transcription:
            ai_response = get_gemini_answer(transcription)

            # Store only the latest interaction (no history)
            st.session_state['latest_interaction'] = {"user": transcription, "ai": ai_response}

            # Display the latest question and AI response
            display_latest_interaction()
        else:
            st.error("❌ Could not transcribe the audio.")
    else:
        st.error("❌ No audio file found. Please record again.")

# Display only the latest user input and AI response
def display_latest_interaction():
    st.markdown("---")
    st.markdown(f"**User**: {st.session_state['latest_interaction']['user']}")
    st.markdown(f"**AI**: {st.session_state['latest_interaction']['ai']}")
    st.markdown("---")

# Main UI
st.title("💬 Voice Input Chat App")
st.write("Record your voice and interact with Gemini.")

# Display the latest interaction only (no history)
if st.session_state['latest_interaction']['user']:
    display_latest_interaction()

# Start and stop recording buttons
if not st.session_state['is_recording']:
    if st.button("🎙️ Start Recording"):
        st.session_state['is_recording'] = True
        record_audio()
else:
    st.write("🔴 Currently recording...")

# Footer to separate different sections
st.markdown("---")
st.write("Created using Streamlit and Gemini 1.5")
