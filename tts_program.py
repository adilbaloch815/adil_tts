"""Interactive text-to-speech tool using pyttsx3.

Features:
- Speak typed text
- Change speaking speed, volume, and voice
- Save spoken text to an audio file
"""

from __future__ import annotations

import sys
from typing import List

import pyttsx3


def list_voices(engine: pyttsx3.Engine) -> List[pyttsx3.voice.Voice]:
    """Print available voices and return the voice list."""
    voices = engine.getProperty("voices")
    print("\nAvailable voices:")
    for idx, voice in enumerate(voices):
        langs = []
        for lang in getattr(voice, "languages", []):
            if isinstance(lang, bytes):
                langs.append(lang.decode(errors="ignore"))
            else:
                langs.append(str(lang))
        lang_text = ", ".join(langs) if langs else "unknown"
        print(f"  [{idx}] {voice.name} | id={voice.id} | languages={lang_text}")
    return voices


def configure_engine(engine: pyttsx3.Engine) -> None:
    """Allow user to configure speed, volume, and voice."""
    current_rate = engine.getProperty("rate")
    current_volume = engine.getProperty("volume")

    print("\n--- Configuration ---")
    print(f"Current speed (rate): {current_rate}")
    new_rate = input("Enter new speed (words per minute) or press Enter to keep current: ").strip()
    if new_rate:
        try:
            engine.setProperty("rate", int(new_rate))
        except ValueError:
            print("Invalid speed. Keeping current value.")

    print(f"Current volume: {current_volume:.2f} (0.0 to 1.0)")
    new_volume = input("Enter new volume (0.0 to 1.0) or press Enter to keep current: ").strip()
    if new_volume:
        try:
            volume_value = float(new_volume)
            if 0.0 <= volume_value <= 1.0:
                engine.setProperty("volume", volume_value)
            else:
                print("Volume out of range. Keeping current value.")
        except ValueError:
            print("Invalid volume. Keeping current value.")

    voices = list_voices(engine)
    selected_voice = input("Select voice index or press Enter to keep current: ").strip()
    if selected_voice:
        try:
            voice_index = int(selected_voice)
            if 0 <= voice_index < len(voices):
                engine.setProperty("voice", voices[voice_index].id)
            else:
                print("Voice index out of range. Keeping current voice.")
        except ValueError:
            print("Invalid voice index. Keeping current voice.")


def speak_text(engine: pyttsx3.Engine, text: str) -> None:
    """Speak text using the engine."""
    engine.say(text)
    engine.runAndWait()


def save_text_to_file(engine: pyttsx3.Engine, text: str) -> None:
    """Save synthesized speech to an audio file."""
    file_path = input("Enter output filename (example: output.mp3): ").strip()
    if not file_path:
        print("No filename provided. Skipping save.")
        return

    engine.save_to_file(text, file_path)
    engine.runAndWait()
    print(f"Saved speech to: {file_path}")


def main() -> None:
    print("Python Text-to-Speech (pyttsx3)")

    try:
        engine = pyttsx3.init()
    except Exception as exc:  # pragma: no cover
        print(f"Could not initialize pyttsx3: {exc}")
        sys.exit(1)

    configure_engine(engine)

    while True:
        print("\n--- Menu ---")
        print("1. Speak text")
        print("2. Reconfigure speed/volume/voice")
        print("3. Quit")

        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            text = input("Type the text you want spoken: ").strip()
            if not text:
                print("No text entered.")
                continue

            speak_text(engine, text)

            should_save = input("Save this speech to a file? (y/n): ").strip().lower()
            if should_save in {"y", "yes"}:
                save_text_to_file(engine, text)

        elif choice == "2":
            configure_engine(engine)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
