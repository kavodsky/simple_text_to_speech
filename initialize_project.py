import os
import requests
from pathlib import Path

ROOT = Path(__file__).parent

def download_file(url, filename):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad responses

    with open(filename, 'wb') as file:
        file.write(response.content)


def initialize_project():
    # Create models directory if it doesn't exist
    models_dir = ROOT.joinpath("models")
    models_dir.mkdir(exist_ok=True)
    print(f"Models directory created/verified at: {models_dir.absolute()}")

    # Base URL for the files
    base_url = "https://huggingface.co/enlyth/baj-tts/resolve/main/models/"

    # Files to download
    files = ["config.json", "david.pth"]

    for file in files:
        file_url = base_url + file
        file_path = models_dir / file
        if file_path.exists():
            print(f"{file} already exists. Skipping download.")
        else:
            print(f"Downloading {file} to {file_path}...")
            download_file(file_url, file_path)

    print("Initialization complete!")


if __name__ == "__main__":
    initialize_project()
