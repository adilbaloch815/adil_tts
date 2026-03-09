# Pyttsx3 Text-to-Speech CLI

A simple interactive Python text-to-speech program using `pyttsx3`.

## Features

- Type text and hear it spoken.
- Change speaking speed (rate).
- Change volume (`0.0` to `1.0`).
- Select from available system voices.
- Save spoken text to an audio file.

## Requirements

- Python 3.8+
- `pyttsx3`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the program:

```bash
python tts_program.py
```

### Program flow

1. Configure speed, volume, and voice.
2. Choose from the menu:
   - `1` Speak text
   - `2` Reconfigure speed/volume/voice
   - `3` Quit
3. Optionally save spoken text to a file when prompted.

## Notes

- Available voices depend on your operating system and installed speech engines.
- Output format support for saved files can vary by platform/driver.
