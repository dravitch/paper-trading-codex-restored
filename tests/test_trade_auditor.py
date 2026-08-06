from datetime import datetime

from examples.trade_auditor_v2 import TradeAuditorV2
from paper_trading_codex.strategies.grid_bot import GridBot


def test_auditor_rejects_a_close_without_public_pair_identifier():
    auditor = TradeAuditorV2(
        [{"type": "CLOSE_TP", "price": 90, "pnl_usd": 10}],
        initial_capital=1_000,
        initial_price=100,
    )

    result = auditor.verify_short_logic_correct()

    assert result["verified_pairs"] == 0
    assert result["is_suspicious"] is True
    assert result["verdict"] == "AUCUNE PAIRE VÉRIFIÉE"


def test_auditor_verifies_all_public_close_event_types_and_fees():
    bot = GridBot(
        {
            "leverage": 2,
            "initial_capital": 1_000,
            "grid_size": 1,
            "max_position_size": 0.30,
            "maker_fee": 0.0005,
            "trading_fee": 0.001,
        }
    )
    bot.initialize(100)
    bot.open_position(100, 102, datetime(2024, 1, 1))
    bot.close_open_positions(90, datetime(2024, 1, 2))
    auditor = TradeAuditorV2(bot.get_audit_trades(), 1_000, 100)

    pairs = auditor.verify_short_logic_correct()
    fees = auditor.verify_fees_exact()

    assert pairs["verified_pairs"] == 1
    assert pairs["verdict"] == "OK"
    assert fees["total_fees_observed"] == fees["total_fees_expected"]
    assert fees["verdict"] == "OK"
