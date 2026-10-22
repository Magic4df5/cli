#!/bin/bash
set -e
export PYTHONPATH=.
pytest --cov=log_analyzer --cov-report=html:htmlcov --cov-report=term
echo "HTML coverage report generated in htmlcov/index.html"