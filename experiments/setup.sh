#!/usr/bin/env bash
# Set up the experiment environment and verify the shared library.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "Installing Python requirements..."
python -m pip install --quiet -r experiments/requirements.txt

echo "Running shared_lib self-tests..."
python -m experiments.shared_lib.test_shared_lib

echo
echo "Environment ready. Recommended run order: D -> A -> B -> C, G -> F -> E, H -> I -> J."
echo "See experiments/STATUS.md for live state."
