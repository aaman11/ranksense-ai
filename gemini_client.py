import os
import re
from dotenv import load_dotenv
import google.generativeai as genai
from prompts import PERSONAS, build_prompt

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

LINE_RE = re.compile(r"^\s*(\d+)[.)]\s*(.+?)\s*[-–—]\s*(.+?)\s*$")

def parse_rankings(text):
    rankings = []
    for line in text.splitlines():
        m = LINE_RE.match(line)
        if m:
            rank, brand, reason = m.groups()
            rankings.append({"rank": int(rank), "brand": brand, "reason": reason})
    return rankings

def call_persona(persona, query):
    system, user = build_prompt(persona, query)
    model = genai.GenerativeModel("gemini-2.5-pro", system_instruction=system)
    resp = model.generate_content(user)
    return {"label": persona["label"], "rankings": parse_rankings(resp.text or "")}

def run_all_personas(query):
    return [call_persona(p, query) for p in PERSONAS]
