"""Oracle rationnel H0004 indépendant du ledger Producteur."""

from __future__ import annotations

from fractions import Fraction


def derive_spot_round_trip(scenario: dict) -> dict:
    base = Fraction(scenario["initial_balances"]["base"])
    quote = Fraction(scenario["initial_balances"]["quote"])
    states = []
    fees = Fraction(0)
    for fill in scenario["fills"]:
        quantity = Fraction(fill["quantity"])
        price = Fraction(fill["price"])
        fee = Fraction(fill["fee_amount"])
        trade_quote = quantity * price
        if fill["side"] == "BUY":
            base += quantity
            quote -= trade_quote + fee
        else:
            base -= quantity
            quote += trade_quote - fee
        fees += fee
        states.append({"base_balance": base, "quote_balance": quote, "fees": fees})
    return {"states": states, "final_base": base, "final_quote": quote, "fees": fees}
