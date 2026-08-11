"""
TVM Subagent: given structured variables, decides which deterministic
tool function to call, and formats the response.
"""

from tvm_tools import solve_pv, solve_fv, solve_rate, solve_n, convert_rate
from formatter import format_answer


def solve_tvm(variables: dict, show_steps: bool = False) -> str:
    """
    variables: dict that may contain any of pv, fv, i, n (numeric or None)
               plus optional 'unknown' key naming which to solve for.
    Returns a formatted answer string.
    """
    pv = variables.get("pv")
    fv = variables.get("fv")
    i = variables.get("i")
    n = variables.get("n")
    unknown = variables.get("unknown")

    if unknown == "fv" or (fv is None and pv is not None and i is not None and n is not None):
        value = solve_fv(pv, i, n)
        return format_answer(
            "FV", value,
            formula="FV = -PV * (1+i)^n",
            substituted=f"FV = -({pv}) * (1+{i})^{n}",
            show_steps=show_steps,
        )

    if unknown == "pv" or (pv is None and fv is not None and i is not None and n is not None):
        value = solve_pv(fv, i, n)
        return format_answer(
            "PV", value,
            formula="PV = -FV / (1+i)^n",
            substituted=f"PV = -({fv}) / (1+{i})^{n}",
            show_steps=show_steps,
        )

    if unknown == "i" or (i is None and pv is not None and fv is not None and n is not None):
        value = solve_rate(pv, fv, n)
        return format_answer(
            "i", value,
            formula="i = (-FV/PV)^(1/n) - 1",
            substituted=f"i = (-({fv})/({pv}))^(1/{n}) - 1",
            show_steps=show_steps,
        )

    if unknown == "n" or (n is None and pv is not None and fv is not None and i is not None):
        value = solve_n(pv, fv, i)
        return format_answer(
            "n", value,
            formula="n = ln(-FV/PV) / ln(1+i)",
            substituted=f"n = ln(-({fv})/({pv})) / ln(1+{i})",
            show_steps=show_steps,
        )

    return ("I need more information to solve this. Please provide any three "
            "of PV, FV, i, n and tell me which one is unknown.")
