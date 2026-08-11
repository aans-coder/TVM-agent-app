"""
Formats tool outputs into user-facing text.
Handles the 'show steps' vs 'final answer only' behavior.
"""


def format_answer(label: str, value: float, formula: str = None,
                   substituted: str = None, show_steps: bool = False) -> str:
    """
    label: e.g. "PV", "FV", "i", "n"
    value: the numeric result
    formula: the general formula used, e.g. "PV = FV / (1+i)^n"
    substituted: the formula with numbers plugged in
    show_steps: if True, show formula + substitution before the answer
    """
    rounded = round(value, 2)

    if not show_steps:
        return f"**{label} = {rounded:,.2f}**"

    parts = []
    if formula:
        parts.append(f"Formula: `{formula}`")
    if substituted:
        parts.append(f"Substituted: `{substituted}`")
    parts.append(f"**{label} = {rounded:,.2f}**")
    return "\n\n".join(parts)
