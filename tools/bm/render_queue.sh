#!/bin/bash
# usage: bash tools/render_queue.sh SCENE...  waits for the current render_direct run, then starts the next list (detached)
cd /home/user/battle-maps/arnold
L="$*"
setsid nohup bash -c "while pgrep -f 'render_direct.sh' >/dev/null; do sleep 15; done; RD_DETACHED=1 bash tools/render_direct.sh $L > logs/render_direct_\$(date +%s).log 2>&1" > /dev/null 2>&1 < /dev/null &
echo queued $L
