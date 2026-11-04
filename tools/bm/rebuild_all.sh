#!/bin/bash
# Rebuild every scene against the final v11 maps and the FINAL timing.json (run from anywhere).
cd /home/user/battle-maps/grant
python3 - <<'PY'
from PIL import Image
Image.open("assets/mississippi_hd_lift.jpg").convert("RGB").resize((2880,1620)).save("assets/media/vx_miss_relief.jpg", quality=92)
PY
python3 tools/vx_make_control.py miss
run() { echo "=== $*"; python3 "$@" 2>&1 | tail -4; }
run tools/gh_inline.py hook-a donelson_hd_lift hook-1 hook-2
run tools/gh_inline.py hook-b donelson_hd_lift hook-3 hook-4
run tools/vk_inline.py m2a vicksburg_hd_lift m2-1 m2-2
run tools/vk_inline.py m2b vicksburg_siege_hd_lift m2-3 m2-3
run tools/vk_inline.py m2c mississippi_hd_lift m2-4 m2-4
run tools/vk_inline.py m2d grandgulf_hd_lift m2-5 m2-6
run tools/vx_inline.py m2e vicksburg_hd_lift m2-7 m2-7
run tools/vx_inline.py m2f vicksburg_hd_lift m2-8 m2-10
run tools/vx_inline.py m2g vicksburg_siege_hd_lift m2-11 m2-12
run tools/m3_build.py m3a richmond m3-1 m3-2
run tools/m3_build.py m3b jamesriver m3-3 m3-4
run tools/m3_build.py m3c petersburg m3-5 m3-5
run tools/m3_build.py m3d petersburg m3-6 m3-7 richmond
run tools/m3_build.py ending tennessee end-1 end-2 mississippi richmond
touch logs/rebuild.done
