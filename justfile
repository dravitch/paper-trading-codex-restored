default: check

lint:
    ruff check paper_trading_codex tests examples

format:
    ruff format paper_trading_codex tests examples
    ruff check paper_trading_codex tests examples --fix

test:
    pytest tests -q

coverage:
    pytest tests -q --cov=paper_trading_codex --cov-branch --cov-report=term-missing

build:
    python -m build --no-isolation

check: lint coverage
