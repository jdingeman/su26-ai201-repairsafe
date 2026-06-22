import json
import os
from datetime import datetime, timezone
from config import LOG_FILE, LLM_MODEL


def log_interaction(question: str, tier: str, response: str) -> None:
    """
    Append a structured record of this interaction to the audit log.

    Writes one JSON line to LOG_FILE and prints a one-line terminal summary.
    Creates the logs/ directory if it does not exist.
    """
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    entry = {
        "timestamp": timestamp,
        "tier": tier,
        "question": question[:300],
        "response_preview": response[:200],
        "response_length": len(response),
        "model": LLM_MODEL,
    }

    log_dir = os.path.dirname(LOG_FILE)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"{timestamp} | {tier.upper():<7} | {len(response)} chars | {question[:60]}")