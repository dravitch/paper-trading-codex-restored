"""
ExchangeSimulator - Simulation d'exécution d'ordres locale.

Moteur local indépendant des endpoints privés d'un fournisseur.
Simule un slippage paramétré et une commission de scénario.

Référence Codex: Partie 1.1.2, Partie 3.2
"""

import logging
from datetime import datetime
from typing import Dict, Optional

import numpy as np

logger = logging.getLogger(__name__)


class ExchangeSimulator:
    """
    Simule l'exécution d'ordres market avec friction réaliste.

    - Slippage paramétré; aucune calibration externe n'est revendiquée
    - Commission de scénario; aucune tarification fournisseur actuelle n'est revendiquée
    - Slippage TOUJOURS défavorable (dégrade le prix, jamais améliore)

    Args:
        slippage_config: {'mean': 0.000342, 'std': 0.000187}
            Valeurs de scénario; leur provenance doit être documentée par l'utilisateur.
        commission_rate: Taux de commission du scénario (défaut 0.001 = 0.1%)
        seed: Seed du générateur local. Obligatoire pour une expérience reproductible.
    """

    def __init__(
        self,
        slippage_config: Dict[str, float],
        commission_rate: float = 0.001,
        seed: Optional[int] = None,
    ):
        self.slippage_mean: float = slippage_config.get("mean", 0.000342)
        self.slippage_std: float = slippage_config.get("std", 0.000187)
        self.commission_rate: float = commission_rate
        self._rng = np.random.default_rng(seed)
        if self.slippage_mean < 0 or self.slippage_std < 0:
            raise ValueError("Slippage parameters must be non-negative")
        if not 0 <= self.commission_rate < 1:
            raise ValueError("commission_rate must be in [0, 1)")

    def _calculate_slippage(self) -> float:
        """
        Calcule un slippage paramétré. TOUJOURS positif (défavorable).

        Returns:
            Slippage en fraction (ex: 0.0003 = 0.03%)
        """
        raw = self._rng.normal(self.slippage_mean, self.slippage_std)
        return abs(raw)  # TOUJOURS défavorable

    def place_market_order(
        self,
        symbol: str,
        side: str,
        amount: float,
        current_price: float,
        timestamp: Optional[datetime] = None,
    ) -> Dict:
        """
        Simule un ordre market avec slippage + commission.

        Args:
            symbol: Paire de trading (ex: 'SOL/USDT')
            side: 'buy' ou 'sell'
            amount: Montant en USD
            current_price: Prix actuel du marché
            timestamp: Horodatage (défaut: now)

        Returns:
            Dict avec executed_price, quantity, commission, timestamp

        Raises:
            ValueError: Si side invalide ou amount <= 0
        """
        if side not in ("buy", "sell"):
            raise ValueError(f"Side invalide: {side}. Attendu 'buy' ou 'sell'.")
        if amount <= 0:
            raise ValueError(f"Amount doit être > 0, reçu: {amount}")
        if current_price <= 0:
            raise ValueError(f"Price doit être > 0, reçu: {current_price}")

        ts = timestamp or datetime.now()
        slippage = self._calculate_slippage()

        # Slippage TOUJOURS défavorable
        if side == "buy":
            executed_price = current_price * (1 + slippage)
        else:
            executed_price = current_price * (1 - slippage)

        # Commission du scénario, sans revendication de calibration fournisseur
        commission = amount * self.commission_rate

        # `amount` est le débit brut, commission incluse pour un achat.
        if side == "buy":
            quantity = (amount - commission) / executed_price
        else:
            quantity = amount / executed_price

        execution = {
            "symbol": symbol,
            "side": side,
            "executed_price": executed_price,
            "quantity": quantity,
            "commission": commission,
            "slippage": slippage,
            "timestamp": ts,
        }

        logger.info(
            "Order executed: %s %s %.2f USD @ %.4f (slip=%.4f%%, fee=%.4f USD)",
            side.upper(),
            symbol,
            amount,
            executed_price,
            slippage * 100,
            commission,
        )

        return execution
