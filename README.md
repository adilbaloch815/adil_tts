# pyttsx3 Text-to-Speech CLI

A simple Python command-line app that:
- asks the user to type text,
- speaks the text aloud,
- saves the speech into an **MP3** file.

## Requirements

- Python 3.9+
- `ffmpeg` installed and available in your `PATH` (used for MP3 encoding)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python tts_pyttsx3.py
```

You will be prompted to:
1. Enter text to speak.
2. Enter an output MP3 filename.

### Optional flags

```bash
python tts_pyttsx3.py --rate 180 --volume 0.9 --voice english
```

- `--rate`: speech rate in words/minute (default: `175`)
- `--volume`: volume from `0.0` to `1.0` (default: `1.0`)
- `--voice`: partial voice name to match (optional)

## Notes

- `pyttsx3` is used for TTS synthesis.
- The app generates a temporary WAV using `pyttsx3`, then converts to MP3 with `pydub` + `ffmpeg`.
