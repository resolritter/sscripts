#!/usr/bin/env python3

import os
import subprocess
import pathlib

previous_run_playlist_url_file_name = ".playlist"

if __name__ == "__main__":
    cwd = pathlib.Path().absolute()
    program_parent_directory = os.path.dirname(__file__)

    try:
        playlist = os.sys.argv[1]
    except IndexError:
        with open(
            os.path.normpath(os.path.join(cwd, previous_run_playlist_url_file_name)),
            "r",
        ) as previous_run_playlist_url_file:
            for line in previous_run_playlist_url_file:
                if line:
                    playlist = line.rstrip()
                    break

    subprocess.call(
        [os.path.join(program_parent_directory, "dump_playlist.sh"), playlist]
    )
    subprocess.call([os.path.join(program_parent_directory, "update_playlist.py"), cwd])
