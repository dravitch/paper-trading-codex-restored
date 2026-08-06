"""
GridBot - Stratégie Grid Short pour Bear Market.

Aligné sur GridBotV3 (Codex Paper Trading - VERSION FINALE).

Conventions du modèle:
- `size` est la quantité contractuelle SOL, levier déjà inclus dans le notionnel
- PnL = (entry - exit) × quantité contractuelle
- ✅ Grille SHORT ascendante (niveaux AU-DESSUS du prix)
- ✅ Fees = size_sol × price × fee_rate
- seuil de liquidation isolée simplifié, dérivé dans METHODS.md
- ✅ Recalcul grille quand prix dépasse max
- ✅ Facteur réduction taille par nombre de positions

Référence: Codex Partie 2.1, 2.3.3, grid_bot.py V3
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class GridBot:
    """Grid Bot Short - 100% configurable via YAML."""

    def __init__(self, config: Dict):
        # Trading
        self.leverage: float = config["leverage"]
        self.grid_size: int = config.get("grid_size", 7)
        self.grid_ratio: float = config.get("grid_ratio", 0.02)
        self.initial_capital: float = config["initial_capital"]
        self.maker_fee: float = config.get("maker_fee", 0.0005)
        self.taker_fee: float = config.get("trading_fee", 0.001)

        # Grille
        self.max_position_size: float = config.get("max_position_size", 0.30)
        self.max_positions: int = config.get("max_positions", self.grid_size)
        self.min_grid_distance: float = config.get("min_grid_distance", 0.01)
        self.adaptive_spacing: bool = config.get("adaptive_spacing", False)

        # Risque
        self.maintenance_margin: float = config.get("maintenance_margin", 0.05)
        self.safety_buffer: float = config.get("safety_buffer", 1.5)
        self.liquidation_loss_fraction: float = config.get(
            "liquidation_loss_fraction", 0.80
        )

        # État
        self.collateral_sol: float = 0.0
        self.initial_collateral_sol: float = 0.0
        self.initial_price: float = 0.0
        self._initialized: bool = False
        self.positions: List[Dict] = []
        self.liquidated: bool = False
        self.grid_levels: List[float] = []
        self.trades: List[Dict] = []
        self.total_fees_paid: float = 0.0
        self.peak_sol: float = 0.0
        self._next_position_id: int = 1

        if self.leverage <= 0:
            raise ValueError("leverage must be positive")
        if self.initial_capital <= 0:
            raise ValueError("initial_capital must be positive")
        if self.grid_size <= 0 or self.max_positions <= 0:
            raise ValueError("grid_size and max_positions must be positive")
        if self.safety_buffer <= 0:
            raise ValueError("safety_buffer must be positive")
        if not 0 <= self.maintenance_margin < 1:
            raise ValueError("maintenance_margin must be in [0, 1)")
        if not 0 <= self.liquidation_loss_fraction <= 1:
            raise ValueError("liquidation_loss_fraction must be in [0, 1]")

    # ================================================================
    # INITIALISATION
    # ================================================================

    def initialize(self, initial_price: float) -> None:
        """Convertit capital USD → SOL et calcule grille initiale."""
        if initial_price <= 0:
            raise ValueError("initial_price must be positive")
        self.initial_price = initial_price
        self.collateral_sol = self.initial_capital / initial_price
        self.initial_collateral_sol = self.collateral_sol
        self.peak_sol = self.collateral_sol
        self._initialized = True
        self.grid_levels = self._calculate_grid_levels(initial_price)

        logger.info(
            "GridBot initialized: %.4f SOL @ $%.2f (leverage=%dx)",
            self.collateral_sol, initial_price, self.leverage,
        )

    # ================================================================
    # GRILLE — SHORT = niveaux AU-DESSUS du prix (V3 Codex)
    # ================================================================

    def _calculate_grid_levels(self, current_price: float) -> List[float]:
        """
        Calcule niveaux de grille POUR SHORT.

        CRITIQUE: SHORT = Vendre en MONTANT
        → Niveaux AU-DESSUS du prix
        → On vend cher, on rachète pas cher

        Exemple: Prix $200, ratio 2%, 3 niveaux
        → Grille: $204, $208.1, $212.3
        """
        levels = []
        level = current_price

        for i in range(self.grid_size):
            spacing = self.grid_ratio
            if self.adaptive_spacing:
                spacing = self.grid_ratio * (1 + i * 0.1)
            spacing = max(spacing, self.min_grid_distance)

            # SHORT: monter AU-DESSUS du prix
            level = level * (1 + spacing)
            levels.append(level)

        return sorted(levels)  # Ascending (plus proche en premier)

    # ================================================================
    # POSITION SIZE — quantité contractuelle SOL
    # ================================================================

    def _calculate_position_size(self, price: float) -> float:
        """
        Calcule la quantité contractuelle en SOL.

        marge allouée = equity × max_position_size × facteur
        notionnel = marge allouée × levier
        quantité = notionnel / prix
        """
        portfolio_value_usd = self.collateral_sol * price

        # Réduction selon positions existantes (V3 Codex)
        position_count_factor = 1.0 - (len(self.positions) * 0.1)
        position_count_factor = max(0.3, position_count_factor)

        available_size = self.max_position_size * position_count_factor
        margin_budget = portfolio_value_usd * available_size
        position_notional = margin_budget * self.leverage

        return position_notional / price

    # ================================================================
    # LIQUIDATION — modèle isolé simplifié
    # ================================================================

    def _calculate_liquidation_price(self, entry_price: float) -> float:
        """
        Seuil d'un short isolé simplifié, sans frais de clôture ni paliers.

        À liquidation: marge initiale + PnL latent = marge de maintenance.
        E*q/L + (E-liq)*q = liq*q*MMR
        donc liq = E*(1 + 1/L)/(1 + MMR).

        Ce seuil n'est pas présenté comme une réplique d'exchange. Le paramètre
        historique `safety_buffer` est conservé pour compatibilité de config,
        mais n'altère plus une identité comptable.
        """
        return entry_price * (1 + (1 / self.leverage)) / (
            1 + self.maintenance_margin
        )

    # ================================================================
    # OPEN POSITION
    # ================================================================

    def _open_position(
        self, entry_price: float, grid_level: float, timestamp: datetime
    ) -> bool:
        """Ouvre position SHORT."""
        if len(self.positions) >= self.max_positions:
            return False

        size_sol = self._calculate_position_size(entry_price)
        if size_sol <= 0:
            return False

        # Frais entrée (V3: size × price × fee_rate)
        entry_fee_usd = size_sol * entry_price * self.maker_fee
        entry_fee_sol = entry_fee_usd / entry_price
        self.collateral_sol -= entry_fee_sol
        self.total_fees_paid += entry_fee_usd

        liq_price = self._calculate_liquidation_price(entry_price)

        position = {
            "position_id": self._next_position_id,
            "entry_price": entry_price,
            "size": size_sol,
            "grid_level": grid_level,
            "liquidation_price": liq_price,
            "entry_fee_usd": entry_fee_usd,
            "leverage": self.leverage,
            "timestamp": timestamp,
        }
        self.positions.append(position)

        # Trade record (champs d'audit complets)
        self.trades.append({
            "type": "OPEN_SHORT",
            "position_id": self._next_position_id,
            "price": entry_price,
            "quantity": size_sol,
            "size_usd": size_sol * entry_price,
            "commission": entry_fee_usd,
            "liq_price": liq_price,
            "leverage": self.leverage,
            "timestamp": timestamp,
        })
        self._next_position_id += 1

        logger.debug(
            "Opened short @ $%.2f, size=%.4f SOL, lev=%.1fx, liq=$%.2f",
            entry_price, size_sol, self.leverage, liq_price,
        )
        return True

    # ================================================================
    # CLOSE POSITION — PnL avec leverage explicite (V3 Codex)
    # ================================================================

    def _close_position(
        self, position: Dict, exit_price: float, timestamp: datetime,
        reason: str = "take_profit",
    ) -> float:
        """
        Ferme position.

        PnL short linéaire:
            gross_pnl_usd = (entry_price - exit_price) × quantity
            net_pnl_usd = gross - exit_fee
            pnl_sol = net_pnl_usd / exit_price
        """
        size_sol = position["size"]

        # Frais sortie (V3: size × price × fee_rate)
        exit_fee_usd = size_sol * exit_price * self.taker_fee

        # Le levier est déjà représenté dans la quantité contractuelle.
        price_change = position["entry_price"] - exit_price
        gross_pnl_usd = price_change * size_sol

        # PnL net
        net_pnl_usd = gross_pnl_usd - exit_fee_usd
        pnl_sol = net_pnl_usd / exit_price

        # Mise à jour collateral
        self.collateral_sol += pnl_sol
        self.total_fees_paid += exit_fee_usd

        if self.collateral_sol > self.peak_sol:
            self.peak_sol = self.collateral_sol

        # Trade record (champs d'audit complets)
        total_fees = position.get("entry_fee_usd", 0) + exit_fee_usd
        close_types = {
            "take_profit": "CLOSE_TP",
            "stop_loss": "CLOSE_SL",
            "mtm": "CLOSE_MTM",
        }
        self.trades.append({
            "type": close_types.get(reason, f"CLOSE_{reason.upper()}"),
            "position_id": position["position_id"],
            "price": exit_price,
            "entry_price": position["entry_price"],
            "exit_price": exit_price,
            "quantity": size_sol,
            "size_usd": size_sol * position["entry_price"],
            "commission": exit_fee_usd,
            "total_commission": total_fees,
            "pnl_usd": net_pnl_usd,
            "pnl_sol": pnl_sol,
            "leverage": position.get("leverage", self.leverage),
            "reason": reason,
            "timestamp": timestamp,
        })

        return net_pnl_usd

    # ================================================================
    # STEP — Boucle principale (alignée V3)
    # ================================================================

    def step(self, current_price: float, timestamp: datetime) -> Dict:
        """Une itération de trading."""
        if not self._initialized:
            self.initialize(current_price)

        if self.liquidated:
            return {
                "liquidated": True, "collateral_sol": self.collateral_sol,
                "price": current_price, "timestamp": timestamp,
                "action": "STOPPED",
            }

        # ÉTAPE 1: Check liquidation
        for position in self.positions[:]:
            if current_price >= position["liquidation_price"]:
                collateral_before = self.collateral_sol
                retained_fraction = 1 - self.liquidation_loss_fraction
                self.collateral_sol *= retained_fraction
                self.liquidated = True

                # Trade record
                liq_size = sum(p["size"] for p in self.positions)
                self.trades.append({
                    "type": "LIQUIDATION",
                    "price": current_price,
                    "quantity": liq_size,
                    "size_usd": liq_size * current_price,
                    "commission": 0,
                    "pnl_usd": -(collateral_before * current_price * 0.8),
                    "pnl_sol": -(collateral_before * 0.8),
                    "loss_pct": self.liquidation_loss_fraction * 100,
                    "timestamp": timestamp,
                })

                self.positions.clear()
                logger.warning(
                    "LIQUIDATED at $%.2f. Collateral: %.4f → %.4f SOL (-%.1f%%)",
                    current_price, collateral_before, self.collateral_sol,
                    self.liquidation_loss_fraction * 100,
                )
                return {
                    "liquidated": True, "collateral_sol": self.collateral_sol,
                    "price": current_price, "timestamp": timestamp,
                    "action": "LIQUIDATED",
                }

        # ÉTAPE 2: Take profit — SHORT: fermer quand prix BAISSE
        for position in self.positions[:]:
            tp_price = position["entry_price"] * (1 - self.grid_ratio)
            if current_price <= tp_price:
                self._close_position(position, current_price, timestamp, "take_profit")
                self.positions.remove(position)

        # ÉTAPE 3: Recalcul grille si prix sort de la zone (V3 + extension)
        # V3 original: recalcul si prix dépasse le max
        # Extension: recalcul aussi si prix descend sous le min (bear market)
        if self.grid_levels:
            if current_price > max(self.grid_levels) * 1.05:
                self.grid_levels = self._calculate_grid_levels(current_price)
            elif current_price < min(self.grid_levels) * 0.90:
                self.grid_levels = self._calculate_grid_levels(current_price)

        # ÉTAPE 4: Ouvrir nouvelles positions (avec exposure guard)
        if len(self.positions) < self.max_positions:
            # Exposure guard: ne pas ouvrir si exposition totale trop élevée
            total_exposure_sol = sum(p["size"] for p in self.positions)
            max_total_exposure = (
                self.collateral_sol
                * self.leverage
                * self.max_position_size
                * self.max_positions
            )
            can_open = total_exposure_sol < max_total_exposure

            if can_open:
                for level in self.grid_levels:
                    distance = abs(current_price - level) / level
                    if distance <= 0.02:
                        if not any(
                            abs(p["entry_price"] - current_price) / current_price < 0.01
                            for p in self.positions
                        ):
                            self._open_position(current_price, level, timestamp)
                            break

        return {
            "liquidated": False, "collateral_sol": self.collateral_sol,
            "price": current_price, "timestamp": timestamp,
            "active_positions": len(self.positions),
        }

    # ================================================================
    # UTILITAIRES
    # ================================================================

    def get_sol_return_pct(self) -> float:
        if self.initial_collateral_sol == 0:
            return 0.0
        return (self.collateral_sol - self.initial_collateral_sol) / self.initial_collateral_sol * 100

    def get_summary(self, current_price: float) -> Dict:
        return {
            "collateral_sol": self.collateral_sol,
            "initial_collateral_sol": self.initial_collateral_sol,
            "sol_return_pct": self.get_sol_return_pct(),
            "usd_value": self.collateral_sol * current_price,
            "initial_usd": self.initial_capital,
            "usd_return_pct": (self.collateral_sol * current_price - self.initial_capital) / self.initial_capital * 100,
            "active_positions": len(self.positions),
            "total_trades": len(self.trades),
            "liquidated": self.liquidated,
            "leverage": self.leverage,
            "total_fees": self.total_fees_paid,
        }

    def close_open_positions(self, current_price: float, timestamp=None) -> int:
        """Ferme toutes les positions ouvertes (mark-to-market fin de backtest)."""
        ts = timestamp or datetime.now()
        closed = 0
        for position in self.positions:
            self._close_position(position, current_price, ts, "mtm")
            closed += 1
        self.positions.clear()
        return closed

    def get_audit_trades(self) -> List[Dict]:
        """Tous les trades au format standard d'audit."""
        return list(self.trades)

    # Backward compat pour tests
    def calculate_grid_levels(self, current_price: float) -> List[float]:
        """Public wrapper pour tests."""
        return self._calculate_grid_levels(current_price)

    def calculate_liquidation_price(self, entry_price: float) -> float:
        """Public wrapper pour tests."""
        return self._calculate_liquidation_price(entry_price)

    def open_position(
        self, entry_price: float, grid_level: float, timestamp: datetime
    ) -> bool:
        """Ouvre une position via l'API publique après initialisation."""
        if not self._initialized:
            raise RuntimeError("initialize must be called before open_position")
        return self._open_position(entry_price, grid_level, timestamp)

    def should_open_position(
        self, current_price: float, active_positions: int,
        max_positions: Optional[int] = None,
    ) -> Tuple[bool, Optional[float]]:
        """Décision d'ouverture (utilisé par tests)."""
        max_pos = max_positions or self.max_positions
        if active_positions >= max_pos:
            return False, None
        if self.liquidated:
            return False, None
        if not self.grid_levels:
            return False, None

        for level in self.grid_levels:
            distance = abs(current_price - level) / level
            if distance <= 0.02:
                if not any(
                    abs(p["entry_price"] - current_price) / current_price < 0.01
                    for p in self.positions
                ):
                    return True, level
        return False, None
