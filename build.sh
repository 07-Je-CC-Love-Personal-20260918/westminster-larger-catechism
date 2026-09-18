#!/usr/bin/env bash
# 一键重建：生成 site/index.html 并做静态校验
set -euo pipefail
cd "$(dirname "$0")/src"
python3 build.py
cd ..
python3 verify.py
