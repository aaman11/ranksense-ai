"""Thin wrapper around google-generativeai."""
import os
import re
from dotenv import load_dotenv
import google.generativeai as genai

from prompts import PERSONAS, build_prompt

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY in your .env file")

genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-pro"  # or "gemini-2.5-flash" for speed

LINE_RE = re.compile(r"^\s*(\d+)[.)]\s*(.+?)\s*[-–—]\s*(.+?)\s*$")


def parse_rankings(text: str) -> list[dict]:
    """Parse 'N. Brand - reason' lines into structured rankings."""
    rankings = []
    for line in text.splitlines():
        m = LINE_RE.match(line)
        if not m:
            continue
        rank, brand, reason = m.groups()
        rankings.append({
            "rank": int(rank),
            "brand": brand.strip(),
            "reason": reason.strip()[:200],
        })
        if len(rankings) >= 5:
            break
    return rankings


def call_persona(persona: dict, query: str) -> dict:
    """Run Gemini once for a single persona; return structured result."""
    system, user = build_prompt(persona, query)
    try:
        model = genai.GenerativeModel(
            MODEL_NAME,
            system_instruction=system,
            generation_config={"temperature": 0.4, "max_output_tokens": 600},
        )
        resp = model.generate_content(user)
        rankings = parse_rankings(resp.text or "")
        return {
            "id": persona["id"],
            "label": persona["label"],
            "rankings": rankings,
            "raw": resp.text,
        }
    except Exception as e:
        return {
            "id": persona["id"],
            "label": persona["label"],
            "rankings": [],
            "error": str(e),
        }


def run_all_personas(query: str) -> list[dict]:
    return [call_persona(p, query) for p in PERSONAS]
