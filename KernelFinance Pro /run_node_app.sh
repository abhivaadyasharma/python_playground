#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
echo "The Node.js desktop build is now legacy."
echo "Launching the unified Python app instead..."
./run_app.sh
