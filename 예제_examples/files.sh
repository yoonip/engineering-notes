#!/usr/bin/env bash
set -eu
pwd                         # 현재 작업 디렉터리
mkdir -p notes
printf 'voltage,current\n3.3,0.02\n' > notes/data.csv
cat notes/data.csv
find notes -type f -name '*.csv'
