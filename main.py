import os
import json
import torch
import streamlit as st
from pathlib import Path, PureWindowsPath
from TTS.utils.synthesizer import Synthesizer
from typing import Dict

ROOT_DIR = Path(__file__).resolve().parent

# Initialize paths and variables
base_model_path = ROOT_DIR.joinpath("models")
config_path = base_model_path.joinpath("config.json")
output_path = ROOT_DIR.joinpath("output")
sample_rate = 22050
synthesizers: Dict[str, Synthesizer] = {}

# Load voice models
with open(ROOT_DIR.joinpath("models.json"), "r") as f:
    models = json.load(f)
    VOICES = {voice["name"]: voice for voice in models["voices"]}


def generate_tts(text: str, voice: str) -> str:
    output_dir = str(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    model_file = base_model_path / VOICES[voice]["model"]
    if not os.path.exists(model_file):
        st.error(f"Model file {VOICES[voice]['model']} does not exist.")
        return None

    if not os.path.exists(config_path):
        st.error(f"Config file {config_path} does not exist.")
        return None

    if voice not in synthesizers:
        synthesizers[voice] = Synthesizer(
            tts_config_path=config_path,
            tts_checkpoint=model_file,
            # use_cuda=use_cuda,
        )
    wav = synthesizers[voice].tts(text)

    output_filename = f"output-{voice}.wav"
    path = os.path.join(output_dir, output_filename)
    synthesizers[voice].save_wav(wav, path)

    return path


def main():
    st.set_page_config(page_title="Text to Speech Synthesizer",
                       page_icon=":material/grid_on:", layout="wide")
    st.title("SimpleTTS")
    # Model selection
    selected_model = st.selectbox("Select model:", list(VOICES.keys()))

    # Text input with clear button
    with st.form(key='text_form', clear_on_submit=True):
        st.session_state.synthesise = st.text_area("Enter text:", height=300)
        st.session_state.submitted = st.form_submit_button(label='Synthesize')


    if st.session_state.submitted:
        if st.session_state.synthesise:
            col1, col2 = st.columns([0.65, 0.35])
            with col1:
                st.write(st.session_state.synthesise)
            with col2:
                with st.spinner(text="In progress..."):
                    output_file = generate_tts(st.session_state.synthesise, selected_model)
                    if output_file:
                        st.success(f"Audio generated: {output_file}")
                        st.audio(output_file)
        else:
            st.warning("Please enter some text to synthesize.")



if __name__ == "__main__":
    main()
