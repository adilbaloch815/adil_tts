"""Interactive text-to-speech CLI using pyttsx3 with MP3 export.

Why this implementation:
- `pyttsx3` can reliably synthesize speech and save to a file.
- On many platforms/backends, direct MP3 output is not supported by `pyttsx3`.
- To guarantee an MP3, this script saves a temporary WAV first, then converts it
  to MP3 using pydub/ffmpeg.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import tempfile

import pyttsx3
from pydub import AudioSegment


def build_engine(rate: int, volume: float, voice: str | None) -> pyttsx3.Engine:
    """Create and configure a pyttsx3 engine."""
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    engine.setProperty("volume", max(0.0, min(1.0, volume)))

    if voice:
        selected_voice = next(
            (v for v in engine.getProperty("voices") if voice.lower() in v.name.lower()),
            None,
        )
        if selected_voice:
            engine.setProperty("voice", selected_voice.id)
        else:
            print(
                f"[warning] Voice '{voice}' not found. Using default voice.",
                file=sys.stderr,
            )

    return engine


def speak_text(engine: pyttsx3.Engine, text: str) -> None:
    """Speak the given text through speakers."""
    engine.say(text)
    engine.runAndWait()


def save_text_as_mp3(engine: pyttsx3.Engine, text: str, output_path: Path) -> None:
    """Save TTS output as MP3 by creating WAV via pyttsx3 then converting."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_wav_path = Path(tmp.name)

    try:
        # Step 1: Create WAV with pyttsx3.
        engine.save_to_file(text, str(tmp_wav_path))
        engine.runAndWait()

        if not tmp_wav_path.exists() or tmp_wav_path.stat().st_size == 0:
            raise RuntimeError("pyttsx3 failed to create a WAV audio file.")

        # Step 2: Convert WAV -> MP3.
        AudioSegment.from_wav(tmp_wav_path).export(output_path, format="mp3")
    finally:
        tmp_wav_path.unlink(missing_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Text-to-speech app with MP3 export")
    parser.add_argument("--rate", type=int, default=175, help="Speech rate (words per minute)")
    parser.add_argument("--volume", type=float, default=1.0, help="Volume between 0.0 and 1.0")
    parser.add_argument(
        "--voice",
        type=str,
        default=None,
        help="Optional partial voice name to select",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    print("=== pyttsx3 Text-to-Speech ===")
    text = input("Enter text to speak: ").strip()
    if not text:
        print("No text entered. Exiting.")
        return 1

    destination = input("Enter output MP3 filename (e.g., output.mp3): ").strip() or "output.mp3"
    output_path = Path(destination)
    if output_path.suffix.lower() != ".mp3":
        output_path = output_path.with_suffix(".mp3")

    engine = build_engine(rate=args.rate, volume=args.volume, voice=args.voice)

    # Speak immediately for interactive feedback.
    speak_text(engine, text)

    try:
        save_text_as_mp3(engine, text, output_path)
    except Exception as exc:
        print(
            "Failed to save MP3. Ensure ffmpeg is installed and available in PATH. "
            f"Details: {exc}",
            file=sys.stderr,
        )
        return 2

    if output_path.exists() and output_path.stat().st_size > 0:
        print(f"Done. Audio saved to: {output_path.resolve()}")
        return 0

    print("MP3 output file was not created.", file=sys.stderr)
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
