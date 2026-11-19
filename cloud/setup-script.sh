#!/usr/bin/env bash
# Execute from a trusted local checkout.
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$HERE/install.py" --global "$@"
