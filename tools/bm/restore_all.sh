#!/usr/bin/env bash
# restore (tint) every film clip listed in a file, 2 workers, detached-safe; log logs/restore_all.log, marker logs/restore_all.done
cd "$(dirname "$0")/.."
LIST=$1; mkdir -p build/frontlines logs; rm -f logs/restore_all.done
work() { while read c; do [ -f build/frontlines/r_${c}_tint.mp4 ] || python3 tools/restore_film.py assets/film/clips/$c.mp4 build/frontlines/r_${c}_tint.mp4 --tint < /dev/null && echo "done $c"; done; }
awk 'NR%2==1' "$LIST" | work &
awk 'NR%2==0' "$LIST" | work &
wait; echo ALLDONE; touch logs/restore_all.done
