import math

import pandas as pd
import pytest

from paper_trading_codex.core.data_loader import (
    DataLoader,
    adapt_config_to_timeframe,
    validate_timeframe_consistency,
)


def test_load_csv_normalizes_columns_and_removes_invalid_rows(tmp_path):
    csv = tmp_path / "prices.csv"
    csv.write_text(
        "date,Open,High,Low,Close,Volume\n"
        "2024-01-01,100,110,90,105,10\n"
        "2024-01-02,100,95,90,105,11\n"
        "2024-01-03,100,110,90,,12\n",
        encoding="utf-8",
    )

    frame = DataLoader.load_csv(str(csv))

    assert list(frame.columns) == ["open", "high", "low", "close", "volume"]
    assert frame.to_dict("records") == [
        {"open": 100, "high": 110, "low": 90, "close": 105.0, "volume": 10}
    ]


def test_load_csv_preserves_datetime_index_when_requested(tmp_path):
    csv = tmp_path / "prices.csv"
    csv.write_text(
        "date,close\n2024-01-01T00:00:00,100\n2024-01-01T01:00:00,101\n",
        encoding="utf-8",
    )

    frame = DataLoader.load_csv(str(csv), reset_index=False)

    assert isinstance(frame.index, pd.DatetimeIndex)
    assert frame["close"].tolist() == [100, 101]


@pytest.mark.parametrize(
    ("contents", "message"),
    [
        ("date,open\n2024-01-01,100\n", "must have 'close'"),
        ("date,close\n2024-01-01,\n", "No valid data"),
    ],
)
def test_load_csv_rejects_unusable_data(tmp_path, contents, message):
    csv = tmp_path / "invalid.csv"
    csv.write_text(contents, encoding="utf-8")

    with pytest.raises(ValueError, match=message):
        DataLoader.load_csv(str(csv))


def test_load_csv_rejects_missing_file(tmp_path):
    with pytest.raises(ValueError, match="File not found"):
        DataLoader.load_csv(str(tmp_path / "missing.csv"))


def test_quality_metrics_are_reproducible():
    frame = pd.DataFrame({"close": [100.0, 101.0, None], "volume": [1, 2, 3]})

    metrics = DataLoader.validate_data_quality(frame)

    assert metrics["total_rows"] == 3
    assert metrics["missing_values"] == 1
    assert metrics["completeness"] == pytest.approx(5 / 6)
    assert metrics["max_price_jump"] == pytest.approx(0.01)
    assert 0 <= metrics["quality_score"] <= 1


def test_quality_metrics_handle_empty_frame():
    assert DataLoader.validate_data_quality(pd.DataFrame()) == {
        "total_rows": 0,
        "missing_values": 0,
        "completeness": 0.0,
        "quality_score": 0.0,
    }


@pytest.mark.parametrize(
    ("frequency", "expected"),
    [("1h", "1h"), ("4h", "4h"), ("1D", "1d"), ("7D", "1w")],
)
def test_infer_timeframe_known_frequencies(frequency, expected):
    frame = pd.DataFrame(
        {"close": [100, 101, 102]},
        index=pd.date_range("2024-01-01", periods=3, freq=frequency),
    )
    assert DataLoader.infer_timeframe(frame) == expected


def test_infer_timeframe_unknown_without_datetime_index():
    assert DataLoader.infer_timeframe(pd.DataFrame({"close": [1, 2, 3]})) == "unknown"


def test_timeframe_rules_return_falsifiable_warnings():
    warnings = validate_timeframe_consistency(
        {"grid_ratio": 0.04, "safety_buffer": 0.5}, "1h"
    )
    assert len(warnings) == 2
    assert "grid_ratio=0.040" in warnings[0]
    assert "safety_buffer=0.5" in warnings[1]
    assert validate_timeframe_consistency({}, "unknown") == []


def test_adapt_config_uses_square_root_of_time_without_mutating_source():
    source = {"grid_ratio": 0.01, "safety_buffer": 1.5, "grid_size": 24}

    adapted = adapt_config_to_timeframe(source, "1h", "1d")

    assert adapted["grid_ratio"] == round(0.01 * math.sqrt(24), 4)
    assert adapted["safety_buffer"] == 8.0
    assert adapted["grid_size"] == 2
    assert source == {"grid_ratio": 0.01, "safety_buffer": 1.5, "grid_size": 24}
    assert adapt_config_to_timeframe(source, "bad", "1d") == source
