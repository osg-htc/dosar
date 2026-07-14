#!/usr/bin/env python3
"""
================================================================================
ASP AI Plotting Assistant
African School of Physics — Kenya 2026

This script connects to an AI assistant that helps you write PyROOT plotting
code using plain English descriptions of what you want.

BEFORE YOU START:
  Replace "replace_me" below with the class token written on the whiteboard.

Usage:
    python3 asp_assistant.py

Requirements:
    Python 3 only — no extra packages needed.
================================================================================
"""

import urllib.request
import urllib.parse
import json
import sys

# ── Configuration ──────────────────────────────────────────────────────────────
# Replace "replace_me" with the token from the whiteboard
PROXY_URL   = "https://asp.travelwith.kids/ask"
CLASS_TOKEN = "replace_me"
# ──────────────────────────────────────────────────────────────────────────────

# ── System prompt ──────────────────────────────────────────
SYSTEM_PROMPT = """You are a physics plotting assistant for students at the African School of Physics.

Students have just completed a Z→mumu dimuon invariant mass analysis on the WLCG grid using HTCondor. They have ROOT histograms (TH1F objects) of the dimuon invariant mass and want to produce publication-quality plots.

Your role:
- Generate complete, runnable PyROOT code in response to plain-English requests
- Always include: axis labels with units (GeV/c²), a descriptive title, and basic formatting
- For peak fitting: use TF1 with a Gaussian signal plus a linear or polynomial background
- Explain each code block briefly so students understand what it does
- If asked to improve a plot iteratively, show only the changed lines and explain what changed
- Never invent ROOT functions that do not exist — if unsure, say so clearly
- Keep responses concise and educational

The students are working on Scientific Linux with ROOT 6 and Python 3 (PyROOT).
Common histogram name: zMass (dimuon invariant mass, range approximately 0-200 GeV)."""
# ──────────────────────────────────────────────────────────────────────────────

def ask_assistant(question):
    """Send a question to the AI proxy and return the response text."""
    payload = json.dumps({
        "prompt": question,
        "token":  CLASS_TOKEN,
        "system": SYSTEM_PROMPT,
    }).encode("utf-8")

    req = urllib.request.Request(
        PROXY_URL,
        data    = payload,
        headers = {"Content-Type": "application/json"},
        method  = "POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["content"][0]["text"]

    except urllib.error.HTTPError as e:
        if e.code == 401:
            return "❌ Wrong class token — check the whiteboard and update CLASS_TOKEN in this script."
        elif e.code == 429:
            return "⏳ Rate limit reached — please wait 10 minutes and try again."
        else:
            return f"❌ HTTP error {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return f"❌ Connection error: {e.reason}. Check your internet connection."
    except (KeyError, IndexError):
        return "❌ Unexpected response from server."
    except Exception as e:
        return f"❌ Unexpected error: {e}"


def print_banner():
    print("=" * 70)
    print("  ASP AI Plotting Assistant")
    print("  African School of Physics — Kenya 2026")
    print("=" * 70)
    print()
    if CLASS_TOKEN == "replace_me":
        print("  ⚠️  You need to set your class token first!")
        print("  Open asp_assistant.py and replace 'replace_me'")
        print("  with the token written on the whiteboard.")
        print()
    print("  Describe your PyROOT plotting problem in plain English.")
    print("  The AI will return complete, runnable PyROOT code.")
    print()
    print("  Example questions:")
    print("  - 'Plot my TH1F histogram h_mee with axis labels and a title'")
    print("  - 'Add a Gaussian fit to the Z peak around 91 GeV'")
    print("  - 'Add the fit parameters and chi-squared to the legend'")
    print("  - 'Change the histogram color to blue and add a grid'")
    print()
    print("  Type 'quit' to exit.")
    print("=" * 70)
    print()


def main():
    print_banner()

    # Warn and exit early if token not set
    if CLASS_TOKEN == "replace_me":
        sys.exit(1)

    while True:
        try:
            question = input("Your question: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            sys.exit(0)

        if not question:
            continue

        if question.lower() in ("quit", "exit", "q", "bye"):
            print("Goodbye!")
            break

        print("\nAsking AI assistant...\n")
        answer = ask_assistant(question)

        print("-" * 70)
        print(answer)
        print("-" * 70)
        print()


if __name__ == "__main__":
    main()
