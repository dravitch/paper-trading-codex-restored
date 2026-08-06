"""
BitgetDataFetcher - Client Bitget en lecture seule.

Adaptateur public legacy; son état réel auprès du fournisseur n'est pas vérifié.
Les endpoints privés sont volontairement non implémentés afin de garantir que ce
projet n'envoie aucun ordre et ne lise aucun compte réel.

Référence Codex: Partie 1.1.2
"""

import logging
import time
from typing import Dict, Optional

import pandas as pd

logger = logging.getLogger(__name__)


class BitgetDataFetcher:
    """
    Client Bitget pour données marché (lecture seule).

    Adaptateur public legacy et non vérifié à la date de la release.
    Ce client expose uniquement des lectures publiques optionnelles. Les endpoints
    privés restent interdits par conception, indépendamment d'une ancienne erreur
    fournisseur 40099 non datée et non reproduite.

    Args:
        api_key: Clé API Bitget
        api_secret: Secret API Bitget
        passphrase: Passphrase API Bitget
        mode: 'demo' (SUSDT) ou 'live' (USDT)
    """

    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
        passphrase: str = "",
        mode: str = "demo",
    ):
        self.mode = mode
        self._client = None
        self._api_key = api_key
        self._api_secret = api_secret
        self._passphrase = passphrase
        self._last_call_time: float = 0
        self._min_interval: float = 0.2  # 200ms entre appels (rate limit)

    def _get_client(self):
        """Lazy init du client CCXT."""
        if self._client is None:
            try:
                import ccxt

                self._client = ccxt.bitget(
                    {
                        "apiKey": self._api_key,
                        "secret": self._api_secret,
                        "password": self._passphrase,
                        "options": {"defaultType": "swap"},
                    }
                )
                logger.info("Client CCXT Bitget initialisé (mode=%s)", self.mode)
            except ImportError:
                logger.warning("ccxt non installé. Mode offline uniquement.")
                raise
        return self._client

    def _rate_limit(self):
        """Rate limiting simple avec backoff."""
        elapsed = time.time() - self._last_call_time
        if elapsed < self._min_interval:
            sleep_time = self._min_interval - elapsed
            time.sleep(sleep_time)
        self._last_call_time = time.time()

    def get_symbol(self, base_symbol: str) -> str:
        """
        Retourne le symbole correct selon le mode.

        Args:
            base_symbol: 'BTC', 'SOL', 'ETH'

        Returns:
            'SBTC/SUSDT:SUSDT' (demo) ou 'BTC/USDT:USDT' (live)
        """
        if self.mode == "demo":
            return f"S{base_symbol}/SUSDT:SUSDT"
        return f"{base_symbol}/USDT:USDT"

    def get_ohlcv(
        self,
        symbol: str,
        timeframe: str = "1h",
        limit: int = 100,
        since: Optional[int] = None,
    ) -> pd.DataFrame:
        """
        Récupère OHLCV public lorsque l'adaptateur optionnel est disponible.

        Args:
            symbol: Paire complète (ex: 'SBTC/SUSDT:SUSDT')
            timeframe: '1m', '5m', '15m', '1h', '4h', '1d'
            limit: Nombre de bougies (max 1000)
            since: Timestamp Unix ms (optionnel)

        Returns:
            DataFrame normalisé: ['open', 'high', 'low', 'close', 'volume']
            Index: DatetimeIndex
        """
        self._rate_limit()
        client = self._get_client()

        logger.info("Fetching OHLCV: %s %s limit=%d", symbol, timeframe, limit)
        ohlcv = client.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)

        df = pd.DataFrame(
            ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

        # Validation types
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        logger.info("OHLCV fetched: %d rows, %s → %s", len(df), df.index[0], df.index[-1])
        return df

    def get_ticker(self, symbol: str) -> Dict:
        """
        Récupère le ticker public lorsque l'adaptateur optionnel est disponible.

        Args:
            symbol: Paire complète

        Returns:
            Dict avec 'last', 'bid', 'ask', 'volume', etc.
        """
        self._rate_limit()
        client = self._get_client()
        return client.fetch_ticker(symbol)

    # =========================================================================
    # ENDPOINTS PRIVÉS INTERDITS PAR CONCEPTION
    # =========================================================================

    def get_balance(self, *args, **kwargs):
        """Endpoint privé volontairement non implémenté."""
        raise NotImplementedError(
            "Private account access is disabled by design. "
            "Utilisez PortfolioManager pour la gestion locale du capital."
        )

    def create_order(self, *args, **kwargs):
        """Endpoint privé volontairement non implémenté."""
        raise NotImplementedError(
            "Private order submission is disabled by design. "
            "Utilisez ExchangeSimulator.place_market_order() pour simulation locale."
        )

    def fetch_positions(self, *args, **kwargs):
        """Endpoint privé volontairement non implémenté."""
        raise NotImplementedError(
            "Private position access is disabled by design. "
            "Utilisez PortfolioManager.get_positions() pour tracking local."
        )
