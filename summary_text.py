#!/usr/bin/env python3
"""
summary_text.py - Extract the spoken text of summary.html for text-to-speech.

Takes the chapter headings and paragraphs from the page (skipping the table of
contents, navigation, figures and captions), drops the "(ilustración N)" pointers
that only make sense on screen, and writes plain UTF-8 text.

Usage:
  python summary_text.py                 # writes summary-audio.txt
  python summary_text.py -o out.txt
  python summary_text.py summary.html -o out.txt
"""

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class SummaryText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.chunks = []          # finished paragraphs / headings
        self.in_section = False   # inside a <section class="cap">
        self.in_figure = False    # inside a <figure> (skipped: images and captions)
        self.buf = None           # text being collected for the current <h1>/<h2>/<p>
        self.title = None

    def handle_starttag(self, tag, attrs):
        cls = (dict(attrs).get("class") or "").split()
        if tag == "section" and "cap" in cls:
            self.in_section = True
        elif tag == "h1" and not self.in_section:
            self.buf = []
        elif tag == "figure":
            self.in_figure = True
        elif tag in ("h2", "p") and self.in_section and not self.in_figure:
            self.buf = []
            self.cur = tag

    def handle_endtag(self, tag):
        if tag == "section":
            self.in_section = False
        elif tag == "figure":
            self.in_figure = False
        elif tag == "span" and self.buf is not None and getattr(self, "cur", None) == "h2":
            # "<span class=num>IV</span>TITLE" -> "IV - TITLE"
            self.buf.append(" - ")
        elif tag in ("h1", "h2", "p") and self.buf is not None:
            text = " ".join("".join(self.buf).split())
            if tag == "h1":
                self.title = text
            elif text:
                self.chunks.append(text)
            self.buf = None
            self.cur = None

    def handle_data(self, data):
        if self.buf is not None:
            self.buf.append(data)


def clean_for_speech(text: str) -> str:
    text = re.sub(r"\s*\((?:ver )?ilustraci[oó]n \d+\)", "", text)
    text = re.sub(r",\s*ilustraci[oó]n \d+:", ":", text)
    text = text.replace(" (ver cuadro)", "")
    text = text.replace(" -> ", " a ")
    return text


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract spoken text from summary.html")
    ap.add_argument("input", nargs="?", default="summary.html")
    ap.add_argument("-o", "--output", default="summary-audio.txt")
    args = ap.parse_args()

    src = Path(args.input)
    if not src.is_file():
        sys.exit(f"Input file not found: {src}")
    parser = SummaryText()
    parser.feed(src.read_text(encoding="utf-8"))
    if not parser.chunks:
        sys.exit("No chapter content found in the page (expected <section class=\"cap\"> blocks).")

    head = "Administración Gerencial. " + (parser.title or "Resumen") + "."
    text = "\n\n".join([head] + [clean_for_speech(c) for c in parser.chunks]) + "\n"
    Path(args.output).write_text(text, encoding="utf-8")
    print(f"{args.output}: {len(parser.chunks)} blocks, {len(text):,} characters")


if __name__ == "__main__":
    main()
