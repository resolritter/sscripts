#!/usr/bin/env python3

from tinydb import TinyDB, where
import time
import os
import json
import argparse
import pathlib


class YoutubePlaylistTracker:
    def __init__(self, db_path):
        self.db = TinyDB(os.path.normpath(os.path.join(db_path, "db.tinydb")))
        self.update_time = time.time()

    def handle_batch(self, batch_file_path):
        with open(batch_file_path) as b_file:
            batch = json.load(b_file)

            for v in filter(lambda x: x is not None, batch["entries"]):
                v["__update_time"] = self.update_time
                self.db.upsert(v, where("id") == v["id"])

            self.check_updated()

    def check_updated(self):
        latest_time = sorted(
            self.db.all(), key=lambda doc: doc["__update_time"], reverse=True
        )[0]["__update_time"]
        for v in self.db.search(where("__update_time") != latest_time):
            print("{} was not updated. [{}]".format(v["title"], v["id"]))


def get_latest_batch_from_folder(folder):
    import re

    try:
        batch = sorted(
            filter(
                lambda file: re.match(
                    r"[0-9]+_[0-9]+_[0-9]+_[0-9]+__HISTORY.json", file
                ),
                os.listdir(folder),
            ),
            reverse=True,
        )[0]
        return os.path.normpath(os.path.join(folder, batch))
    except IndexError:
        exit(print("No batch json file on folder {}.".format(folder)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Only check")
    parser.add_argument(
        "folder",
        nargs="?",
        help="The playlist folder (has historical playlist information in tinydb.json)",
        default=pathlib.Path().absolute(),
    )
    parser.add_argument(
        "batch",
        nargs="?",
        help="""
        Path to JSON dump from Youtube-DL to update the database with.
        If left unset, it expects a file in the format year_month_date_timestamp.json to be in the folder, and it will pick the latest one (sorted in descending order by file name) as the batch.
        """,
        default=None,
    )
    args = parser.parse_args()

    db = YoutubePlaylistTracker(args.folder)
    if args.check:
        db.check_updated()
    else:
        batch = args.batch
        if batch is None:
            batch = get_latest_batch_from_folder(args.folder)
            # exit(print(batch))

        db.handle_batch(batch)
