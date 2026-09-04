.PHONY: install test run clean

install:
    python -m venv .venv
    . .venv/bin/activate && pip install -r requirements.txt

test:
    . .venv/bin/activate && pytest --cov=. --cov-report=term-missing --cov-fail-under=70

run:
    . .venv/bin/activate && python vane_space_init.py

clean:
    rm -rf .venv __pycache__ .pytest_cache .coverage htmlcov
