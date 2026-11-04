#!/bin/bash
# Voice cloning (Chatterbox, MIT) in its own venv: it pins numpy<2 / torch 2.6 and must not touch the Kokoro setup.
# ~4 min install + ~3 GB model on first use. Then:
#   /home/user/cb-venv/bin/python tts/clone_voice.py REF.wav OUT.wav "text" [exaggeration 0.45] [cfg 0.45]
set -e
V=/home/user/cb-venv
[ -x $V/bin/python ] || python3 -m venv $V
$V/bin/python -c "import chatterbox" 2>/dev/null && { echo "chatterbox already installed"; exit 0; }
$V/bin/pip install -q --upgrade pip
$V/bin/pip install -q torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cpu
$V/bin/pip install -q chatterbox-tts
$V/bin/python -c "import chatterbox, torch; print('chatterbox ok, torch', torch.__version__)"
