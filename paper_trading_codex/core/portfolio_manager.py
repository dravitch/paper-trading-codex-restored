"""
PortfolioManager - Gestion unifiée du portfolio.

Un seul objet pour balance + positions + trades + equity curve.
Les frais sont comptés une fois à l'entrée et une fois à la sortie.
État atomique : tout se passe dans place_market_order().

Référence Codex: Partie 1.2.3, Partie 3.3
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class PortfolioManager:
    """
    Portfolio unifié : balance + positions + performance tracking.

    Règles critiques:
    - Fees prélevées à l'entry ET à l'exit (0.1% × 2 = 0.2% total)
    - État jamais désynchronisé (atomicité)
    - Equity curve trackée pour Sharpe ratio

    Args:
        initial_capital: Capital initial en USD
    """

    def __init__(self, initial_capital: float):
        self.initial_capital: float = initial_capital
        self.balance: float = initial_capital  # USD disponible
        self.positions: Dict[str, Dict] = {}  # {symbol: position_data}
        self.trade_history: List[Dict] = []
        self.equity_curve: List[Dict] = []

    def place_market_order(
        self,
        symbol: str,
        side: str,
        amount: float,
        current_price: float,
        simulator,  # ExchangeSimulator
        timestamp: Optional[datetime] = None,
    ) -> Dict:
        """
        Place un ordre via simulator ET met à jour le portfolio.

        ATOMICITÉ : simulation + mise à jour balance/positions en un seul appel.

        Args:
            symbol: Paire de trading
            side: 'buy' ou 'sell'
            amount: Montant en USD
            current_price: Prix marché actuel
            simulator: Instance ExchangeSimulator
            timestamp: Horodatage optionnel

        Returns:
            Dict avec détails de l'exécution

        Raises:
            ValueError: Si sell sans position existante ou balance insuffisante
        """
        ts = timestamp or datetime.now()

        # Validation
        if side == "buy" and amount > self.balance:
            raise ValueError(
                f"Balance insuffisante: {self.balance:.2f} USD < {amount:.2f} USD"
            )
        if side == "sell" and symbol not in self.positions:
            raise ValueError(f"Aucune position {symbol} à fermer")

        # Simuler ordre (slippage + commission entry)
        execution = simulator.place_market_order(
            symbol, side, amount, current_price, ts
        )

        if side == "buy":
            # Contrat du simulateur: `amount` est le débit brut, frais inclus;
            # la quantité reçue vaut (amount - commission) / prix exécuté.
            # Débiter `amount + commission` compterait la commission deux fois.
            self.balance -= amount

            # Créer ou accumuler position
            if symbol in self.positions:
                # Averaging: recalculer prix moyen pondéré
                pos = self.positions[symbol]
                old_value = pos["quantity"] * pos["entry_price"]
                new_value = execution["quantity"] * execution["executed_price"]
                total_qty = pos["quantity"] + execution["quantity"]
                pos["entry_price"] = (old_value + new_value) / total_qty
                pos["quantity"] = total_qty
            else:
                self.positions[symbol] = {
                    "entry_price": execution["executed_price"],
                    "quantity": execution["quantity"],
                    "timestamp": ts,
                    "entry_commission": execution["commission"],
                }

        elif side == "sell":
            position = self.positions[symbol]

            # Valeur de sortie basée sur la position réelle
            exit_value = position["quantity"] * execution["executed_price"]
            entry_value = position["quantity"] * position["entry_price"]
            gross_pnl = exit_value - entry_value

            # Commission exit basée sur valeur de sortie (pas le montant paramètre)
            exit_commission = exit_value * simulator.commission_rate
            net_pnl = gross_pnl - exit_commission

            # Mettre à jour balance (récupérer valeur de sortie - commission)
            self.balance += exit_value - exit_commission

            # Supprimer position
            del self.positions[symbol]

            execution["commission"] = exit_commission
            execution["gross_pnl"] = gross_pnl
            execution["net_pnl"] = net_pnl

        # Logger trade
        self.trade_history.append(
            {
                "symbol": symbol,
                "side": side,
                "amount": amount,
                **execution,
            }
        )

        return execution

    def get_total_equity(self, current_prices: Dict[str, float]) -> float:
        """
        Calcule l'equity totale = balance + valeur positions ouvertes.

        Args:
            current_prices: {symbol: price} pour évaluer les positions

        Returns:
            Equity totale en USD
        """
        equity = self.balance

        for symbol, position in self.positions.items():
            price = current_prices.get(symbol, position["entry_price"])
            equity += position["quantity"] * price

        # Track equity curve
        self.equity_curve.append(
            {
                "timestamp": datetime.now(),
                "equity": equity,
                "balance": self.balance,
                "positions_value": equity - self.balance,
            }
        )

        return equity

    def get_positions(self) -> Dict[str, Dict]:
        """Retourne copie des positions ouvertes."""
        return dict(self.positions)

    def get_trade_count(self) -> int:
        """Nombre total de trades exécutés."""
        return len(self.trade_history)

    def get_total_fees_paid(self) -> float:
        """Total des commissions payées (entry + exit)."""
        return sum(t.get("commission", 0) for t in self.trade_history)

    def get_summary(self, current_prices: Dict[str, float]) -> Dict:
        """
        Résumé complet du portfolio.

        Args:
            current_prices: Prix actuels pour évaluation

        Returns:
            Dict avec equity, pnl, trades, fees, positions
        """
        equity = self.get_total_equity(current_prices)
        return {
            "equity": equity,
            "balance": self.balance,
            "pnl_usd": equity - self.initial_capital,
            "pnl_pct": (equity - self.initial_capital) / self.initial_capital * 100,
            "total_trades": self.get_trade_count(),
            "total_fees": self.get_total_fees_paid(),
            "open_positions": len(self.positions),
            "positions": self.get_positions(),
        }
