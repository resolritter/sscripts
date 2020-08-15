#!/bin/bash

set -e

fname="$(date +"%y_%m_%d_%s")__HISTORY"

playlist="$1"
if [ "$playlist" ]; then
  echo "$playlist" > .playlist
else
  playlist=$(cat .playlist)
fi

youtube-dl --dump-single-json --ignore-errors "$playlist" > "$fname.json"
