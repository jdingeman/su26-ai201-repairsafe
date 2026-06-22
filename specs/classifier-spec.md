# Spec: `classify_safety_tier()`

**File:** `safety.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Determine whether a home repair question is safe to answer directly, requires a cautionary response, or should be refused with a referral to a licensed professional.

---

## Input / Output Contract

**Input:**

| Parameter  | Type  | Description                     |
| ---------- | ----- | ------------------------------- |
| `question` | `str` | The user's home repair question |

**Output:** `dict`

| Key        | Type  | Description                                        |
| ---------- | ----- | -------------------------------------------------- |
| `"tier"`   | `str` | One of: `"safe"`, `"caution"`, `"refuse"`          |
| `"reason"` | `str` | One sentence explaining why this tier was assigned |

---

## Design Decisions

_Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours._

---

### Tier definitions

_Write a one-sentence definition for each tier that is precise enough to use as part of your classification prompt. Vague definitions produce inconsistent classifications._

**safe:**

```
Routine maintenance and low-risk repairs that most homeowners can complete with basic tools and patience, requires no permit or processional license, and there is no risk of injury, fire or flooding.
```

**caution:**

```
Repairs doable for a motivated homeowner, but where mistakes have real cost or mild risk of injury, or where something can go meaningfully wrong.
```

**refuse:**

```
Repairs where an amateur mistake can cause fire, flooding, structural damage, serious injury, or death, or repairs that require a licensed professional and a permit to assess and correct.
```

---

### Classification approach

_How will the LLM classify the question? Will you give it just the tier definitions, or also examples (few-shot)? Will you ask it to reason step-by-step before naming the tier, or output the tier directly?_

_Consider: what happens when a question is genuinely ambiguous — e.g., "can I replace my own outlets?" Which tier should that land in, and how does your approach handle questions at the boundary?_

```
The LLM will use a combination of definitions, few-shot examples and reasoning before labeling the tier. The examples anchor known boundary cases, and reasoning handles novel cases not covered by the examples.
```

---

### Output format

_How will the LLM communicate the tier and reason back to you? Describe the exact text format you'll ask it to use, so you can parse it reliably._

_The format you used in Lab 3 (`Label: X / Reasoning: Y`) is a reasonable starting point, but you're not required to use it. Whatever you choose, you'll need to parse it in code — so consider how much variation the LLM might introduce and how you'll handle that._

```
The LLM will communicate the tier and reason back in this form:
Reasoning: <1-2 sentences>
Tier: <safe|caution|refuse>
Reason: <1 sentence for the user>
```

---

### Prompt structure

_Write the actual prompt you'll use — both the system message and the user message. Don't describe it — write it. Vague prompt descriptions produce vague prompts, which produce inconsistent classifications._

**System message:**

```
You are a home repair safety classifier. Classify each question into exactly one tier:

SAFE: Routine maintenance, low-risk repairs, no permit required, no injury/fire/flood risk.
CAUTION: Doable for a homeowner, but mistakes have real cost or mild injury risk.
REFUSE: Amateur mistakes can cause fire, flooding, structural damage, serious injury, or death; OR requires a licensed professional and permit.

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
Reason: <one sentence for the user>
```

**User message:**

```
Q: {question}
```

---

### Caution/refuse boundary

_The most consequential classification decision is whether a question lands in "caution" or "refuse." Write down your rule for this boundary — one sentence. Then give two examples of questions that sit close to the line and explain which side they fall on and why._

```
Classify as refuse if an amateur mistake could plausibly cause fire, flooding, structural damage, or serious injury, OR if the repair legally requires a permit or licensed professional — regardless of how the user frames the difficulty.

"Replace existing GFCI outlet" → caution (same location, no new wiring, recoverable mistake)
"Add a new outlet in my garage" → refuse (new circuit, panel involvement, permit required)
```

---

### Fallback behavior

_What does your function return if the LLM response can't be parsed — e.g., if it produces free-form prose instead of your expected format? What happens when tier validation against `VALID_TIERS` fails?_

_Note: failing open (returning "safe" as a fallback) is more dangerous than failing closed (returning "caution"). Which makes more sense here, and why?_

```
Return caution on parse failure. This is the safer default — caution always routes the user to advisory guidance rather than either full help or professional referral, so it degrades gracefully.
```

---

## Implementation Notes

_Fill this in after implementing, before moving to Milestone 2._

**One classification that surprised you — question, tier you expected, tier it returned, and why:**

```
The classification on changing the faucet surprised me just because it doesn't seem like a fix that could cause catastrophic damage if the user just does so carefully, as they should with any repair. So I thought it would return safe, but the tier was returned as proceed with caution because it seems like the LLM interprets it as needing much more attention to detail that doing a drywall patch. It makes sense, but it's interesting how it blurs the lines.
```

**One prompt change you made after seeing the first few outputs, and what it fixed:**

```
I removed the word "motivated" from the prompt since I didn't want there to be a subjective interpretation on who is considered a motivated homeowner. The user should interpret the response with an objective viewpoint and not by how motivated they feel as skills levels can vary intensely between homeowners who share the same level of motivation.
```
