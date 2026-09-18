#!/usr/bin/env bash
# 一键重建：生成 site/index.html，跑静态校验与 SVG 版面校验
set -euo pipefail
cd "$(dirname "$0")/src"
python3 build.py
cd ..
python3 verify.py
python3 svgcheck.py
