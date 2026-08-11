"""
Orchestrator: receives raw chat text, uses an LLM to extract structured
TVM variables, then routes to the TVM subagent.
"""

import json
import streamlit as st
from anthropic import Anthropic
from tvm_agent import solve_tvm

client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

EXTRACTION_PROMPT = """You are a variable extractor for a Time Value of Money (TVM) solver.
Given a user's question, extract the following as JSON, using this sign convention:
outflows (money paid out / deposited) are NEGATIVE, inflows (money received) are POSITIVE.

Return ONLY valid JSON with these keys (use null if not given or not applicable):
{
  "pv": <number or null>,
  "fv": <number or null>,
  "i": <number or null, as a decimal e.g. 0.06 for 6%>,
  "n": <number or null>,
  "unknown": <"pv" | "fv" | "i" | "n" | null>,
  "show_steps": <true if user asks to see steps/formula/working, else false>
}

User question: "{question}"
"""


def extract_variables(question: str) -> dict:
    message = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=300,
        messages=[{"role": "user", "content": EXTRACTION_PROMPT.format(question=question)}],
    )
    text = message.content[0].text.strip()
    # Strip markdown code fences if the model adds them
    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json", "", 1).strip()
    return json.loads(text)


def handle_message(question: str) -> str:
    try:
        variables = extract_variables(question)
    except Exception:
        return ("I couldn't understand the numbers in your question. "
                "Could you rephrase it with clear values for PV, FV, i, and n?")

    show_steps = variables.pop("show_steps", False)
    return solve_tvm(variables, show_steps=show_steps)
