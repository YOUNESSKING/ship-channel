#!/bin/bash
# Render the animation tests, add their sound, join them into out/ALL_TESTS.mp4.
# Order: test 1 (old synth sound), test 1 (new ElevenLabs sound), test 4 (rich), test 2, test 3.
set -e
cd "$(dirname "$0")"; mkdir -p out
mux(){ ffmpeg -y -loglevel error -i "$1" -i "$2" -map 0:v -map 1:a -c:v copy -af "loudnorm=I=-16:TP=-1.5:LRA=11" -c:a aac -b:a 192k -shortest "$3"; }
for k in t1 t2 t3 t4; do (cd work/$k && npx -y hyperframes@0.8.188 render --fps 30 --quality high --output ../../out/$k.silent.mp4 > ../../out/$k.log 2>&1); done
mux out/t1.silent.mp4 work/t1/sfx.wav    out/test1_lockon_oldsound.mp4
mux out/t1.silent.mp4 work/t1/sfx_el.wav out/test1_lockon_newsound.mp4
mux out/t2.silent.mp4 work/t2/sfx.wav    out/test2_gauge.mp4
mux out/t3.silent.mp4 work/t3/sfx.wav    out/test3_options.mp4
mux out/t4.silent.mp4 work/t4/sfx.wav    out/test4_rich_lockon.mp4
rm -f out/*.silent.mp4 out/*.log out/test1_lockon.mp4
# 1 s title card before each part
i=0; : > out/list.txt
for f in test1_lockon_oldsound "test 1 - old sound (synth)" test1_lockon_newsound "test 1 - new sound (ElevenLabs)" test4_rich_lockon "test 4 - rich version" test2_gauge "test 2 - gauge" test3_options "test 3 - options"; do
  if [ $((i%2)) -eq 0 ]; then v=$f; else
    ffmpeg -y -loglevel error -f lavfi -i color=c=black:s=1280x720:r=30:d=1.2 -f lavfi -i anullsrc=r=44100:cl=stereo -t 1.2 -vf "drawtext=fontfile=../lib/fonts/$(ls ../lib/fonts | grep -i jost | head -1):text='$f':fontcolor=0xC9A45C:fontsize=30:x=(w-tw)/2:y=(h-th)/2" -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k out/card_$i.mp4
    ffmpeg -y -loglevel error -i out/$v.mp4 -c:v libx264 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 44100 out/n_$i.mp4
    echo "file 'card_$i.mp4'" >> out/list.txt; echo "file 'n_$i.mp4'" >> out/list.txt; fi
  i=$((i+1)); done
ffmpeg -y -loglevel error -f concat -safe 0 -i out/list.txt -c copy out/ALL_TESTS.mp4
rm -f out/card_*.mp4 out/n_*.mp4 out/list.txt
ls -la out
