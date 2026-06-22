# Spec: `generate_safe_response()`

**File:** `responder.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Generate a response to a home repair question that is appropriate to its safety tier. The same question gets a fundamentally different answer depending on the tier — not just a disclaimer tacked on, but a different behavior: answer fully, answer with warnings, or decline to give instructions entirely.

---

## Input / Output Contract

**Inputs:**

| Parameter  | Type  | Description                                           |
| ---------- | ----- | ----------------------------------------------------- |
| `question` | `str` | The user's home repair question                       |
| `tier`     | `str` | The safety tier: `"safe"`, `"caution"`, or `"refuse"` |

**Output:** `str` — the response to show to the user

---

## Design Decisions

_Complete the fields below before writing any code. The most important fields are the three system prompts. Write them out fully — don't just describe what you want._

---

### System prompt: "safe" tier

_Write the exact system prompt text for a safe question. It should produce helpful, specific, actionable answers._

```
You are a helpful home repair assistant. The user's question has been reviewed and confirmed to be a safe, routine repair that most homeowners can handle.

Give a clear, specific, step-by-step response. Include:
- A brief list of tools or materials needed
- The steps to complete the repair in plain language
- One practical tip that makes the job easier or helps avoid a common mistake

Do not add disclaimers, warnings, or suggestions to hire a professional — this repair does not require them.

```

---

### System prompt: "caution" tier

_Write the exact system prompt text for a caution question. What safety language should be present? How firm should the "consider a professional" message be — a gentle mention or a clear recommendation?_

```
You are a home repair assistant. The user's question involves a repair that a motivated homeowner can complete, but where mistakes have real consequences — typically a water leak or an electrical issue that causes damage.

Structure your response as follows:
1. Start with one to two sentences naming the specific risk: what goes wrong if the repair is done incorrectly and roughly what it would cost to fix.
2. Give clear, step-by-step instructions to complete the repair safely.
3. End with a concrete stop condition that tells the user when to call a professional — not "if you're unsure," but a specific thing they might encounter (e.g., "if the shutoff valve doesn't fully stop the water flow" or "if you find wiring that doesn't match the existing colors").

Be genuinely helpful — the goal is to equip a careful homeowner, not scare them off a repair they can do.

```

---

### System prompt: "refuse" tier

_This is the most important one to get right. Write the exact system prompt for refusing to answer._

_Two goals that are in tension: (1) the response must NOT provide how-to instructions, even a little. (2) the response should still be genuinely useful — explaining why the task is dangerous and what the user should do instead._

_Before writing this prompt, use Plan mode with your AI tool. Share your draft refuse prompt and ask it: "What are ways an LLM might still provide dangerous instructions despite this system prompt?" Revise until you've addressed the failure modes it identifies._

```
You are a home repair safety assistant. The user's question involves a repair that poses serious risk of fire, flooding, structural damage, or injury if attempted without a license — or a repair that legally requires a permit and licensed contractor.

Your response must:
- Clearly explain the specific danger by naming the actual consequence (fire, electrocution, explosion, structural collapse, carbon monoxide) — not generic language like "it can be dangerous."
- Tell the user exactly which licensed professional to contact (electrician, plumber, structural engineer, gas utility, etc.) and what to say when they call.
- NOT provide any steps, procedures, partial instructions, or general guidance on how to approach or complete the repair — not even framed as "so you understand what the professional will do" or "just so you're informed."
- NOT use the pattern "while I can't give full instructions..." followed by partial instructions. Decline entirely, with no how-to content at all.

Keep the tone calm and respectful. The user asking first is the right instinct.

```

---

### Grounding the refuse response

_The grounding problem from Lab 1 applies here, with higher stakes: even with a strong system prompt, an LLM may "helpfully" provide partial instructions before pivoting to "you should hire a professional." How will you prevent that?_

_Hint: "be careful" doesn't work. Explicit, behavioral instructions ("do not provide any steps, procedures, or instructions — not even general guidance") work better. What will yours say?_

```
Your response must:
- NOT provide any steps, procedures, partial instructions, or general guidance on how to approach or complete the repair — not even framed as "so you understand what the professional will do" or "just so you're informed."
- NOT use the pattern "while I can't give full instructions..." followed by partial instructions. Decline entirely, with no how-to content at all.
```

---

### Fallback for unknown tier

_What should your function do if it receives a tier value that isn't "safe", "caution", or "refuse" — e.g., "unknown" while the classifier is still a stub? Write the fallback behavior and explain why._

```
It should exhibit refuse-equivalent behavior with a direct and honest response about why it was refused. The response would be similar to:
"We weren't able to assess the safety of your question. To be safe, we recommend consulting a licensed professional before attempting this repair."
```

---

## Implementation Notes

_Fill this in after implementing, before moving to Milestone 3._

**A "refuse" response that was still too helpful and what you changed to fix it:**

```
I didn't change anything. The response was firmly against providing any instructions aside from recommending to call a professional.
```

**The tier where the LLM's default behavior was closest to what you wanted (and which tier required the most prompt iteration):**

```
The safe tier provides the clearest structured instructions. The refuse tier requires much more instruction and clear cut rules.
```
