import os
import requests

CLAUDE_API_URL = os.getenv("CLAUDE_API_URL", "https://api.anthropic.com/v1/complete")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")


def call_claude(prompt, max_tokens=1000, temperature=0.2):
    if not CLAUDE_API_KEY:
        raise RuntimeError("CLAUDE_API_KEY is not set")

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": CLAUDE_API_KEY,
    }
    payload = {
        "model": "claude-3.5-sonic",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens_to_sample": max_tokens,
        "temperature": temperature,
    }
    resp = requests.post(CLAUDE_API_URL, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["completion"] if "completion" in data else data.get("response")
