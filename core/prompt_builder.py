def build_prompt(*, text: str, audience: str, tone: str, target_length: int, formality: int) -> str:
    # target_length as character goal-ish guidance (model is free-form)
    length_hint = (
        "Short" if target_length < 250 else "Medium" if target_length < 800 else "Long"
    )

    formality_desc = (
        "Very formal" if formality >= 80 else
        "Formal" if formality >= 60 else
        "Semi-formal" if formality >= 40 else
        "Casual" if formality >= 20 else
        "Very casual"
    )

    return f"""
You are a world-class writing assistant.
Rewrite the following text to match the specified audience and tone.

Audience: {audience}
Tone: {tone}
Formality level: {formality_desc}
Target length: {length_hint} (aim for ~{target_length} characters, but prioritize clarity.)

Requirements:
- Preserve the original meaning.
- Improve clarity and flow.
- Avoid adding facts not present in the original.
- Output only the rewritten text (no commentary).

Original text:
{text}
""".strip()

