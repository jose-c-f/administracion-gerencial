#!/usr/bin/env python3
"""
txt2mp3.py - Convert a .txt file into an .mp3 audio file using Microsoft Edge
neural voices (via the edge-tts package). No API key required.

Usage
-----
  python txt2mp3.py 05.txt                    # interactive voice menu
  python txt2mp3.py 05.txt -v 3               # pick voice #3 from the menu
  python txt2mp3.py 05.txt -v es-MX-JorgeNeural
  python txt2mp3.py 05.txt -o lesson.mp3 --rate +10% --pitch -2Hz
  python txt2mp3.py --list-voices             # built-in shortlist
  python txt2mp3.py --list-voices --all       # every voice edge-tts knows
  python txt2mp3.py --list-voices --lang en   # all voices for a language

Install
-------
  python -m pip install --user edge-tts
"""

import argparse
import asyncio
import sys
import time
from pathlib import Path

try:
    import edge_tts
except ImportError:
    sys.exit("edge-tts is not installed. Run:  python -m pip install --user edge-tts")


# Curated shortlist shown in the interactive menu. Add or remove entries freely;
# any voice name from `--list-voices --all` works.
VOICES = [
    # (voice id,                 label)
    ("es-ES-AlvaroNeural",       "Spanish (Spain)     - Alvaro, male"),
    ("es-ES-ElviraNeural",       "Spanish (Spain)     - Elvira, female"),
    ("es-ES-XimenaNeural",       "Spanish (Spain)     - Ximena, female"),
    ("es-MX-JorgeNeural",        "Spanish (Mexico)    - Jorge, male"),
    ("es-MX-DaliaNeural",        "Spanish (Mexico)    - Dalia, female"),
    ("es-AR-TomasNeural",        "Spanish (Argentina) - Tomas, male"),
    ("es-AR-ElenaNeural",        "Spanish (Argentina) - Elena, female"),
    ("es-CO-GonzaloNeural",      "Spanish (Colombia)  - Gonzalo, male"),
    ("es-CO-SalomeNeural",       "Spanish (Colombia)  - Salome, female"),
    ("es-US-AlonsoNeural",       "Spanish (US)        - Alonso, male"),
    ("es-US-PalomaNeural",       "Spanish (US)        - Paloma, female"),
    ("en-US-AndrewNeural",       "English (US)        - Andrew, male"),
    ("en-US-AvaNeural",          "English (US)        - Ava, female"),
    ("en-US-BrianNeural",        "English (US)        - Brian, male"),
    ("en-US-EmmaNeural",         "English (US)        - Emma, female"),
    ("en-GB-RyanNeural",         "English (UK)        - Ryan, male"),
    ("en-GB-SoniaNeural",        "English (UK)        - Sonia, female"),
]

DEFAULT_VOICE = VOICES[0][0]


def print_shortlist() -> None:
    print("\nAvailable voices:")
    for i, (vid, label) in enumerate(VOICES, start=1):
        print(f"  {i:2d}. {label:<40} [{vid}]")
    print()


async def print_all_voices(lang: str | None) -> None:
    voices = await edge_tts.list_voices()
    voices.sort(key=lambda v: v["ShortName"])
    for v in voices:
        if lang and not v["Locale"].lower().startswith(lang.lower()):
            continue
        print(f"  {v['ShortName']:<36} {v['Gender']:<7} {v['Locale']}")


def choose_voice_interactively() -> str:
    print_shortlist()
    while True:
        try:
            raw = input(f"Choose a voice [1-{len(VOICES)}] (Enter = 1): ")
        except EOFError:
            sys.exit("\nNo input available. Pass the voice with -v (e.g. -v 1) when not running interactively.")
        raw = raw.strip().lstrip("﻿")  # PowerShell pipes may prepend a BOM
        if raw == "":
            return DEFAULT_VOICE
        if raw.isdigit() and 1 <= int(raw) <= len(VOICES):
            return VOICES[int(raw) - 1][0]
        # Allow typing a full voice id directly.
        if "-" in raw and raw.endswith("Neural"):
            return raw
        print("  Invalid choice, try again.")


def resolve_voice(value: str) -> str:
    """Accept a menu number or a full voice id."""
    if value.isdigit():
        idx = int(value)
        if 1 <= idx <= len(VOICES):
            return VOICES[idx - 1][0]
        sys.exit(f"Voice number must be between 1 and {len(VOICES)}.")
    return value


def read_text(path: Path) -> str:
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    sys.exit(f"Could not decode {path} as UTF-8 or Windows-1252.")


async def synthesize(text: str, voice: str, out: Path, rate: str, pitch: str, volume: str) -> None:
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, volume=volume)
    await communicate.save(str(out))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a text file to MP3 using Microsoft Edge neural voices.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", nargs="?", help="path to the .txt file")
    parser.add_argument("-o", "--output", help="output .mp3 path (default: same name as input)")
    parser.add_argument("-v", "--voice", help="menu number (e.g. 3) or full voice id (e.g. es-MX-JorgeNeural)")
    parser.add_argument("--rate", default="+0%", help="speaking rate, e.g. -10%% or +20%% (default +0%%)")
    parser.add_argument("--pitch", default="+0Hz", help="pitch shift, e.g. -5Hz or +10Hz (default +0Hz)")
    parser.add_argument("--volume", default="+0%", help="volume, e.g. -20%% or +30%% (default +0%%)")
    parser.add_argument("--retries", type=int, default=3, help="attempts before giving up (default 3)")
    parser.add_argument("--retry-delay", type=int, default=5, help="seconds to wait between attempts (default 5)")
    parser.add_argument("--list-voices", action="store_true", help="print the voice shortlist and exit")
    parser.add_argument("--all", action="store_true", help="with --list-voices: show every voice")
    parser.add_argument("--lang", help="with --list-voices --all: filter by locale prefix, e.g. es or en-GB")
    args = parser.parse_args()

    if args.list_voices:
        if args.all or args.lang:
            asyncio.run(print_all_voices(args.lang))
        else:
            print_shortlist()
        return

    if not args.input:
        parser.error("input file is required (or use --list-voices)")

    src = Path(args.input)
    if not src.is_file():
        sys.exit(f"Input file not found: {src}")

    text = read_text(src).strip()
    if not text:
        sys.exit("Input file is empty.")

    voice = resolve_voice(args.voice) if args.voice else choose_voice_interactively()
    out = Path(args.output) if args.output else src.with_suffix(".mp3")
    out.parent.mkdir(parents=True, exist_ok=True)

    print(f"Input : {src}  ({len(text):,} characters)")
    print(f"Voice : {voice}  rate={args.rate} pitch={args.pitch} volume={args.volume}")
    print(f"Output: {out}")
    print("Synthesizing...", end=" ", flush=True)

    last_error = None
    for attempt in range(1, args.retries + 1):
        try:
            asyncio.run(synthesize(text, voice, out, args.rate, args.pitch, args.volume))
            last_error = None
            break
        except Exception as exc:  # dropped connection, no audio, bad rate/pitch format, etc.
            last_error = exc
            out.unlink(missing_ok=True)  # never leave a partial file behind
            if attempt < args.retries:
                print(f"\nAttempt {attempt} failed ({type(exc).__name__}: {exc}). Retrying in {args.retry_delay}s...",
                      end=" ", flush=True)
                time.sleep(args.retry_delay)

    if last_error is not None:
        sys.exit(f"\nFailed after {args.retries} attempts: {type(last_error).__name__}: {last_error}\n"
                 "Check the voice id (see --list-voices --all) and your internet connection.")

    size_kb = out.stat().st_size / 1024
    print(f"done ({size_kb:,.0f} KB).")


if __name__ == "__main__":
    main()
