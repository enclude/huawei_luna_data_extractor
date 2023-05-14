#!/bin/bash
set -e
exec python3 huaweisolar.py &
exec python3 -m http.server
