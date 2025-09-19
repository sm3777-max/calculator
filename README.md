# Command-line Calculator

## Overview
Small command-line calculator with a REPL interface supporting addition, subtraction, multiplication and division. Includes tests and CI that enforces 100% test coverage.

## Setup (Linux / macOS)
```bash
# from project root
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


python -m calculator.cli
# Example inputs:
# add 2 3
# * 4 5
# div 10 2
# help
# exit

pytest --maxfail=1 --disable-warnings -q --cov=calculator --cov-report=term
# To enforce 100% locally:
coverage run -m pytest
coverage report --fail-under=100

cat > requirements.txt <<'EOF'
pytest
pytest-cov
coverage
