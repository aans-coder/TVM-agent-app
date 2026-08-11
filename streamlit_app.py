"""
Deterministic TVM (Time Value of Money) calculation tools.
Sign convention: outflows negative, inflows positive.
All functions are pure, testable, and independent of any LLM.
"""

import math


def solve_fv(pv: float, i: float, n: float) -> float:
    """
    Solve for Future Value given Present Value, interest rate per period, and n periods.
    FV = -PV * (1 + i)^n   (sign flips because PV outflow -> FV inflow, or vice versa)
    """
    return -pv * (1 + i) ** n


def solve_pv(fv: float, i: float, n: float) -> float:
    """
    Solve for Present Value given Future Value, interest rate per period, and n periods.
    PV = -FV / (1 + i)^n
    """
    return -fv / (1 + i) ** n


def solve_rate(pv: float, fv: float, n: float) -> float:
    """
    Solve for periodic interest rate i given PV, FV, and n.
    i = (-FV/PV)^(1/n) - 1
    """
    if pv == 0:
        raise ValueError("PV cannot be zero when solving for rate.")
    ratio = -fv / pv
    if ratio <= 0:
        raise ValueError("PV and FV must have opposite signs under standard convention.")
    return ratio ** (1 / n) - 1


def solve_n(pv: float, fv: float, i: float) -> float:
    """
    Solve for number of periods n given PV, FV, and interest rate i.
    n = ln(-FV/PV) / ln(1+i)
    """
    if pv == 0:
        raise ValueError("PV cannot be zero when solving for n.")
    ratio = -fv / pv
    if ratio <= 0:
        raise ValueError("PV and FV must have opposite signs under standard convention.")
    return math.log(ratio) / math.log(1 + i)


def convert_rate(rate: float, from_type: str, to_type: str, m: int = 1) -> float:
    """
    Convert between nominal, effective, and force-of-interest rates.

    from_type/to_type options: "nominal", "effective", "force"
    m = compounding frequency per year (required for nominal <-> effective).

    Formulas:
      effective from nominal:  (1 + nominal/m)^m - 1
      nominal from effective:  m * ((1+effective)^(1/m) - 1)
      force from effective:    ln(1 + effective)
      effective from force:    e^force - 1
    """
    valid_types = {"nominal", "effective", "force"}
    if from_type not in valid_types or to_type not in valid_types:
        raise ValueError(f"Types must be one of {valid_types}")

    if from_type == to_type:
        return rate

    # Step 1: convert 'from_type' to effective annual rate
    if from_type == "nominal":
        effective = (1 + rate / m) ** m - 1
    elif from_type == "force":
        effective = math.exp(rate) - 1
    else:  # already effective
        effective = rate

    # Step 2: convert effective annual rate to 'to_type'
    if to_type == "effective":
        return effective
    elif to_type == "nominal":
        return m * ((1 + effective) ** (1 / m) - 1)
    elif to_type == "force":
        return math.log(1 + effective)


def equation_of_value(cash_flows: list[tuple[float, float]], i: float, comparison_date: float) -> float:
    """
    Solve the equation of value: sum all cash flows (amount, time) moved
    to the comparison_date at rate i, return the net value at that date.

    cash_flows: list of (amount, time) tuples, e.g. [(-1000, 0), (1200, 2)]
    i: interest rate per period
    comparison_date: the time point to value everything at

    Returns the net value at comparison_date (should be 0 if flows balance
    an unknown you're solving for externally).
    """
    total = 0.0
    for amount, time in cash_flows:
        total += amount * (1 + i) ** (comparison_date - time)
    return total
