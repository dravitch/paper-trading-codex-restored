"""
PerformanceTracker - Métriques de performance.

Sharpe, Sortino, Calmar, Max Drawdown, Win Rate, Profit Factor.
La fréquence d'annualisation est un paramètre obligatoire du protocole expérimental.

Référence Codex: Partie 3.3.2
"""

import logging
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class PerformanceTracker:
    """
    Calcule les métriques de performance sur une equity curve.

    Annualisation: √365 pour crypto (marché 24/7/365).

    Args:
        risk_free_rate: Taux sans risque annuel (défaut 0.04 = 4%)
        periods_per_year: Périodes pour annualisation (défaut 365 pour daily crypto)
    """

    def __init__(
        self,
        risk_free_rate: float = 0.04,
        periods_per_year: int = 365,
    ):
        if periods_per_year <= 0:
            raise ValueError("periods_per_year must be positive")
        self.risk_free_rate = risk_free_rate
        self.periods_per_year = periods_per_year

    def calculate_returns(self, equity_curve: pd.Series) -> pd.Series:
        """Calcule les rendements périodiques."""
        if not isinstance(equity_curve, pd.Series):
            raise TypeError("equity_curve must be a pandas Series")
        if not equity_curve.empty and (equity_curve <= 0).any():
            raise ValueError("equity_curve values must be positive")
        return equity_curve.pct_change().dropna()

    def sharpe_ratio(self, equity_curve: pd.Series) -> float:
        """
        Sharpe Ratio annualisé.

        Formule: (mean_return - rf) / std_return × √periods

        > 1 = bon, > 2 = excellent, > 3 = suspect en crypto
        """
        returns = self.calculate_returns(equity_curve)
        if len(returns) < 2 or returns.std() == 0:
            return 0.0

        rf_per_period = self.risk_free_rate / self.periods_per_year
        excess_returns = returns - rf_per_period

        return float(
            excess_returns.mean()
            / excess_returns.std()
            * np.sqrt(self.periods_per_year)
        )

    def sortino_ratio(self, equity_curve: pd.Series) -> float:
        """
        Sortino annualisé, avec MAR égal au taux sans risque périodique.

        Downside deviation = sqrt(mean(min(R - MAR, 0)^2)). La moyenne porte
        sur toutes les périodes, y compris celles sans déficit. Cette convention
        est explicite afin d'éviter les variantes silencieuses de la métrique.
        """
        returns = self.calculate_returns(equity_curve)
        if len(returns) < 2:
            return 0.0

        rf_per_period = self.risk_free_rate / self.periods_per_year
        excess_returns = returns - rf_per_period

        downside = np.minimum(excess_returns.to_numpy(dtype=float), 0.0)
        downside_deviation = float(np.sqrt(np.mean(np.square(downside))))
        if downside_deviation == 0:
            return float("inf") if excess_returns.mean() > 0 else 0.0

        return float(
            excess_returns.mean()
            / downside_deviation
            * np.sqrt(self.periods_per_year)
        )

    def max_drawdown(self, equity_curve: pd.Series) -> float:
        """
        Maximum Drawdown (en fraction, pas en %).

        Pire chute du pic au creux.
        """
        if len(equity_curve) < 2:
            return 0.0

        cummax = equity_curve.cummax()
        drawdown = (equity_curve - cummax) / cummax
        return float(abs(drawdown.min()))

    def calmar_ratio(self, equity_curve: pd.Series) -> float:
        """
        Calmar Ratio = rendement annualisé composé / maximum drawdown.

        Le nombre de rendements observés fixe la durée de la série. Cette
        définition évite de confondre moyenne arithmétique annualisée et CAGR.
        """
        returns = self.calculate_returns(equity_curve)
        if len(returns) < 2:
            return 0.0

        n_periods = len(returns)
        annual_return = (
            (float(equity_curve.iloc[-1]) / float(equity_curve.iloc[0]))
            ** (self.periods_per_year / n_periods)
            - 1
        )
        mdd = self.max_drawdown(equity_curve)

        if mdd == 0:
            return float("inf") if annual_return > 0 else 0.0

        return float(annual_return / mdd)

    def win_rate(self, trades: List[Dict]) -> float:
        """Pourcentage de trades gagnants."""
        if not trades:
            return 0.0
        winners = sum(1 for t in trades if t.get("pnl_usd", t.get("pnl_sol", 0)) > 0)
        return winners / len(trades) * 100

    def profit_factor(self, trades: List[Dict]) -> float:
        """Gains totaux / Pertes totales."""
        gains = sum(
            t.get("pnl_usd", t.get("pnl_sol", 0))
            for t in trades
            if t.get("pnl_usd", t.get("pnl_sol", 0)) > 0
        )
        losses = abs(
            sum(
                t.get("pnl_usd", t.get("pnl_sol", 0))
                for t in trades
                if t.get("pnl_usd", t.get("pnl_sol", 0)) < 0
            )
        )
        if losses == 0:
            return float("inf") if gains > 0 else 0.0
        return gains / losses

    def calculate_all(
        self,
        equity_curve: pd.Series,
        trades: Optional[List[Dict]] = None,
    ) -> Dict:
        """
        Calcule toutes les métriques d'un coup.

        Args:
            equity_curve: Série de valeurs equity
            trades: Liste de trades (optionnel, pour win_rate/profit_factor)

        Returns:
            Dict avec toutes les métriques
        """
        metrics = {
            "sharpe_ratio": self.sharpe_ratio(equity_curve),
            "sortino_ratio": self.sortino_ratio(equity_curve),
            "max_drawdown_pct": self.max_drawdown(equity_curve) * 100,
            "calmar_ratio": self.calmar_ratio(equity_curve),
            "total_return_pct": (
                (equity_curve.iloc[-1] - equity_curve.iloc[0])
                / equity_curve.iloc[0]
                * 100
                if len(equity_curve) > 0
                else 0.0
            ),
        }

        if trades:
            closing_trades = [
                t
                for t in trades
                if t.get("type")
                in ("CLOSE_TP", "CLOSE_SL", "CLOSE_MTM", "LIQUIDATION")
            ]
            metrics["win_rate_pct"] = self.win_rate(closing_trades)
            metrics["profit_factor"] = self.profit_factor(closing_trades)
            metrics["total_trades"] = len(trades)
            metrics["closing_trades"] = len(closing_trades)

        return metrics
