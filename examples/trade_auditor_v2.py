"""Auditeur déterministe du journal public produit par :class:`GridBot`."""

from __future__ import annotations

import math
from typing import Any


CLOSE_TYPES = {"CLOSE_TP", "CLOSE_SL", "CLOSE_MTM"}


def load_trades_from_bot(bot_instance: Any) -> list[dict]:
    """Copie sérialisable du journal public, sans modifier le bot."""
    result = []
    for trade in bot_instance.get_audit_trades():
        result.append(
            {
                key: value.isoformat() if hasattr(value, "isoformat") else value
                for key, value in trade.items()
            }
        )
    return result


class TradeAuditorV2:
    """Contrôles comptables; zéro paire vérifiée est toujours un échec."""

    def __init__(
        self,
        trades: list[dict],
        initial_capital: float,
        initial_price: float,
        maker_fee: float = 0.0005,
        taker_fee: float = 0.001,
    ):
        self.trades = trades
        self.initial_capital = initial_capital
        self.initial_price = initial_price
        self.maker_fee = maker_fee
        self.taker_fee = taker_fee
        self.opens = [trade for trade in trades if trade.get("type") == "OPEN_SHORT"]
        self.closes = [trade for trade in trades if trade.get("type") in CLOSE_TYPES]

    def verify_win_rate_probability(self) -> dict:
        """Compare le win rate au seuil conventionnel explicite p0=0,5.

        Ce test ne prouve ni fraude ni rentabilité. Il rapporte un écart à une
        hypothèse nulle choisie, au moyen d'une probabilité binomiale bilatérale.
        """
        if not self.closes:
            return {"error": "Aucun trade fermé"}
        n = len(self.closes)
        wins = sum(trade.get("pnl_usd", 0) > 0 for trade in self.closes)
        tail_low = sum(math.comb(n, k) for k in range(0, wins + 1)) / 2**n
        tail_high = sum(math.comb(n, k) for k in range(wins, n + 1)) / 2**n
        p_value = min(1.0, 2 * min(tail_low, tail_high))
        p_hat = wins / n
        z = 1.959963984540054
        denominator = 1 + z**2 / n
        center = (p_hat + z**2 / (2 * n)) / denominator
        margin = (
            z
            * math.sqrt(p_hat * (1 - p_hat) / n + z**2 / (4 * n**2))
            / denominator
        )
        return {
            "n_trades": n,
            "n_wins": wins,
            "n_losses": n - wins,
            "win_rate_observed": p_hat * 100,
            "null_win_rate": 50.0,
            "p_value": p_value,
            "ci_95_lower": (center - margin) * 100,
            "ci_95_upper": (center + margin) * 100,
            "rejects_p0_0_5": p_value < 0.05,
        }

    def verify_fees_exact(self) -> dict:
        """Recalcule les commissions par type d'événement, sans les réutiliser."""
        observed = sum(float(trade.get("commission", 0)) for trade in self.trades)
        expected = 0.0
        for trade in self.trades:
            notional = abs(float(trade.get("quantity", 0))) * float(
                trade.get("price", 0)
            )
            if trade.get("type") == "OPEN_SHORT":
                expected += notional * self.maker_fee
            elif trade.get("type") in CLOSE_TYPES:
                expected += notional * self.taker_fee
        difference = observed - expected
        valid = math.isclose(observed, expected, rel_tol=1e-12, abs_tol=1e-12)
        return {
            "total_fees_observed": observed,
            "total_fees_expected": expected,
            "abs_difference": difference,
            "is_suspicious": not valid,
            "critical_error": not valid,
            "verdict": "OK" if valid else "ERREUR CALCUL",
        }

    def verify_short_logic_correct(self) -> dict:
        """Apparie les événements et vérifie le signe du PnL brut attendu."""
        opens = {
            trade.get("position_id"): trade
            for trade in self.opens
            if trade.get("position_id") is not None
        }
        incoherent = []
        verified = 0
        for close in self.closes:
            position_id = close.get("position_id")
            opened = opens.get(position_id)
            if opened is None:
                continue
            verified += 1
            entry = float(opened["price"])
            exit_price = float(close["price"])
            pnl = float(close.get("pnl_usd", 0))
            # Frais peuvent rendre négatif un faible mouvement favorable; seul un
            # mouvement défavorable avec PnL positif est nécessairement incohérent.
            if entry <= exit_price and pnl > 0:
                incoherent.append(
                    {"position_id": position_id, "entry": entry, "exit": exit_price, "pnl": pnl}
                )
        missing = len(self.closes) - verified
        suspicious = bool(incoherent) or missing > 0 or verified == 0
        if verified == 0:
            verdict = "AUCUNE PAIRE VÉRIFIÉE"
        elif missing:
            verdict = f"{missing} PAIRE(S) MANQUANTE(S)"
        elif incoherent:
            verdict = f"{len(incoherent)} INCOHÉRENT(S)"
        else:
            verdict = "OK"
        return {
            "total_closes": len(self.closes),
            "verified_pairs": verified,
            "missing_pairs": missing,
            "incoherent_count": len(incoherent),
            "incoherent_trades": incoherent,
            "is_suspicious": suspicious,
            "verdict": verdict,
        }

    def generate_report(self) -> str:
        """Retourne un résumé textuel sans interprétation de performance."""
        if not self.trades:
            return "AUDIT TRADES\nAucun trade"
        fees = self.verify_fees_exact()
        pairs = self.verify_short_logic_correct()
        return "\n".join(
            [
                "AUDIT TRADES",
                f"Frais: {fees['verdict']} (écart {fees['abs_difference']:+.12f} USD)",
                f"Paires: {pairs['verdict']} ({pairs['verified_pairs']} vérifiée(s))",
            ]
        )
