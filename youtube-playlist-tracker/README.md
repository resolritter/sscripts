# Info

This program builds an embedded TinyDB database with video metadata information
from a playlist.

## Requires

- Youtube-DL
- Bash
- Unix's `date`, `echo`, `cat` commands
- Python3 and the following dependencies
  - `tinydb`

# Usage

# Direct usage

`main.py [playlist_url]`

This command invokes other executables in this same folder.

Note: If you already have a `.playlist` file in the current directory, the
`[playlist]` argument can be omitted.

# Doing it separately with the individual executables

## 1. Dump the JSON information from a Youtube Playlist with Youtube-DL

`dump_playlist.sh [playlist_url]`

Note: If you already have a `.playlist` file in the current directory, the
`[playlist]` argument can be omitted.

It will create a file with the name
`{YEAR}_{MONTH}_{DAY}_{TIMESTAMP}__HISTORY.json` containing the playlist's
metadata, as well as a `.playlist` file in the same directory which saves the
URL of the last dumped playlist.

## 2. Update the playlist's database

`update_playlist.py [folder where you dumped the playlist]`

Note: If you're already at the dump folder, the argument can be omitted.

Run `update_playlist.py --help` for the full usage guide.
