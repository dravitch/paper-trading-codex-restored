"""
Benchmarks corrects pour validation Grid Bot.

Buy & Hold et Sell & Hold avec calculs précis.
Aligné sur Codex Paper Trading.
"""

from typing import Dict

import pandas as pd


class Benchmarks:
    """
    Calcule les benchmarks Buy & Hold et Sell & Hold.

    Used pour comparer performance du Grid Bot.
    """

    def __init__(
        self,
        initial_capital: float,
        initial_price: float,
        leverage: float = 1.0,
        trading_fee: float = 0.001,
    ):
        """
        Args:
            initial_capital: Capital initial en USD
            initial_price: Prix initial SOL/USD
            leverage: Levier pour Sell & Hold
            trading_fee: Frais de trading (0.001 = 0.1%)
        """
        self.initial_capital = initial_capital
        self.initial_price = initial_price
        self.leverage = leverage
        self.trading_fee = trading_fee
        self.initial_sol = initial_capital / initial_price

    def buy_and_hold(self, prices: pd.Series) -> pd.Series:
        """
        Buy & Hold: Achète SOL au début et garde.

        Formule simple:
            valeur(t) = initial_sol × prix(t)

        Args:
            prices: Série de prix SOL/USD

        Returns:
            Série de valeurs USD dans le temps
        """
        return prices * self.initial_sol

    def sell_and_hold(self, prices: pd.Series, trading_fee: float = None) -> pd.Series:
        """
        Sell & Hold: Short avec levier constant.

        Simulation d'un short unique:
        1. Position = (capital × leverage) / prix_initial
        2. PnL = (prix_initial - prix_actuel) / prix_initial × leverage
        3. Valeur = capital × (1 + PnL) - fees

        Args:
            prices: Série de prix SOL/USD
            trading_fee: Override des frais (optionnel)

        Returns:
            Série de valeurs USD dans le temps
        """
        fee = trading_fee if trading_fee is not None else self.trading_fee

        # Position size en SOL
        position_size = (self.initial_capital * self.leverage) / self.initial_price

        # Frais d'entrée (une seule fois)
        entry_fee = position_size * self.initial_price * fee

        # Variation de prix en %
        price_changes = (self.initial_price - prices) / self.initial_price

        # PnL avec levier
        pnl_pct = price_changes * self.leverage

        # Valeur du portfolio
        values = self.initial_capital * (1 + pnl_pct) - entry_fee

        return pd.Series(values.squeeze(), index=prices.index)

    def sell_and_hold_sol(self, prices: pd.Series) -> pd.Series:
        """Sell & Hold mesuré en SOL accumulé."""
        return self.sell_and_hold(prices) / prices

    def compare(self, prices: pd.Series, strategy_values: pd.Series) -> Dict:
        """
        Compare la stratégie aux benchmarks.

        Args:
            prices: Série de prix
            strategy_values: Série de valeurs USD de la stratégie

        Returns:
            Dict avec métriques de comparaison
        """
        bh = self.buy_and_hold(prices)
        sh = self.sell_and_hold(prices)

        strat_final = float(strategy_values.iloc[-1])
        bh_final = float(bh.iloc[-1])
        sh_final = float(sh.iloc[-1])

        return {
            "strategy_final_usd": strat_final,
            "strategy_return_pct": (strat_final - self.initial_capital) / self.initial_capital * 100,
            "buy_hold_final_usd": bh_final,
            "buy_hold_return_pct": (bh_final - self.initial_capital) / self.initial_capital * 100,
            "sell_hold_final_usd": sh_final,
            "sell_hold_return_pct": (sh_final - self.initial_capital) / self.initial_capital * 100,
            "beats_buy_hold": strat_final > bh_final,
            "beats_sell_hold": strat_final > sh_final,
            "strategy_above_sell_hold": strat_final > sh_final,
        }
