#!/usr/bin/env bash
# Writes the API keys from the environment settings into the key files the tools read.
# Never prints a key. Files are chmod 600 and git-ignored.
set -u
put() { # put VAR file...
  local v="${!1:-}"
  if [ -z "$v" ]; then echo "$1: NOT SET"; return; fi
  for f in "${@:2}"; do umask 077; printf '%s' "$v" > "$f"; done
  echo "$1: ok (${#v} chars)"
}
T="$(cd "$(dirname "$0")" && pwd)"
put RUNPOD_API_KEY ~/.rp_key "$T/.rp_key"
put FAL_KEY ~/.fal_key
put ELEVENLABS_API_KEY ~/.el_key
put ELEVENLABS_API_KEY_2 ~/.el_key2
put FIRECRAWL_API_KEY ~/.firecrawl_key
