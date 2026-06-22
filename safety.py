import re

from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, VALID_TIERS

_client = Groq(api_key=GROQ_API_KEY)

_SYSTEM_MESSAGE = """You are a home repair safety classifier. Classify each question into exactly one tier:

SAFE: Routine maintenance, low-risk repairs, no permit required, no injury/fire/flood risk.
CAUTION: Doable for a motivated homeowner, but mistakes have real cost or mild injury risk.
REFUSE: Amateur mistakes can cause fire, flooding, structural damage, serious injury, or death; OR requires a licensed professional and permit. If the reasoning mentions risk of explosion, electrocution, fire, or carbon monoxide — even as a possible outcome of a mistake — the tier must be refuse, not caution.

Examples:
Q: How do I patch a small hole in drywall?
Reasoning: Cosmetic repair, no structural or utility risk, basic tools only.
Tier: safe
Reason: Low-risk cosmetic repair requiring only basic tools.

Q: How do I replace my existing kitchen faucet?
Reasoning: Involves shutting off water and reconnecting supply lines. A mistake means a leak, which is real but manageable. No permit needed.
Tier: caution
Reason: Water connection work with real but recoverable failure consequences.

Q: How do I add a new electrical outlet to my wall?
Reasoning: Adding a new circuit requires running wire to the panel. Panel and circuit work can cause fire or electrocution. Requires permit and licensed electrician.
Tier: refuse
Reason: New circuit work requires licensed electrician; amateur mistakes risk fire or electrocution.

For each question: briefly reason through the risk, then output:
Reasoning: <one or two sentences>
Tier: <safe|caution|refuse>
Reason: <one sentence for the user>"""

_FALLBACK = {"tier": "caution", "reason": "Could not parse classifier response; defaulting to caution."}


def classify_safety_tier(question: str) -> dict:
    """
    Classify a home repair question into one of three safety tiers.

    Returns a dict with:
      - "tier"   : str — one of "safe", "caution", "refuse"
      - "reason" : str — a brief explanation of why this tier was assigned
    """
    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": _SYSTEM_MESSAGE},
            {"role": "user", "content": f"Q: {question}"},
        ],
    )

    text = response.choices[0].message.content
    if not text:
        return _FALLBACK

    tier_match = re.search(r"(?i)^Tier:\s*(safe|caution|refuse)\s*$", text, re.MULTILINE)
    reason_match = re.search(r"(?i)^Reason:\s*(.+)", text, re.MULTILINE)

    if not tier_match or not reason_match:
        return _FALLBACK

    tier = tier_match.group(1).lower()
    if tier not in VALID_TIERS:
        return _FALLBACK

    return {"tier": tier, "reason": reason_match.group(1).strip()}
