#!/usr/bin/env bash
# bake_all.sh : bakes today + LGM dark relief for every Video-01 map (one at a time; resumable: skips finished)
cd "$(dirname "$0")/.."
PY=./venv/bin/python
while read id lat lon z S; do
  for v in now lgm; do
    s=0; [ $v = lgm ] && s=$S
    [ -f assets/${id}_${v}_hd_ref.jpg ] && continue
    $PY tools/mkjson.py ${id}_${v} $lat $lon $z $s
    SEA_LEVEL=$s $PY tools/bake_hd.py ${id}_${v} 2.5 && echo "baked ${id}_${v}"
  done
done <<'EOF'
beringia 63 -175 6 -120
doggerland 55 4 6 -120
black_sea 43.5 34 7 -100
mediterranean 40.2 4 7 -120
red_sea 20.5 40 6 -120
carpentaria -9 140 6 -120
gulf_mexico 26.5 -88 7 -120
sundaland 2 108 6 -120
world 28 80 4 -120
EOF
echo ALLDONE
