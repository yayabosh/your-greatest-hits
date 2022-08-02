import csv
from typing import NamedTuple

from last_fm import get_top_tracks
from spotify import create_playlist, get_playlist_id, update_playlist


class User(NamedTuple):
    name: str
    last_fm_username: str
    threshold: int
    moniker: str


# Get users from users.csv and create a list of User objects
users = []
with open("tables/users.csv", newline="") as f:
    reader = csv.DictReader(row for row in f if not row.startswith("#"))
    for row in reader:
        users.append(
            User(
                row["name"],
                row["last_fm_username"],
                int(row["threshold"]),
                row["moniker"],
            )
        )

for user in users:
    get_top_tracks(user)
    playlist_id = get_playlist_id(user)
    if playlist_id is None:
        playlist_id = create_playlist(user)

    update_playlist(playlist_id)
