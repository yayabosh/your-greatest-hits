import csv  # For parsing tables/users.csv
from typing import List, NamedTuple  # For creating a named tuple representing a user

from gmail import send_email  # For sending an email to a user
from last_fm import get_tracks_above_threshold  # For getting the top tracks for a user
from spotify import (
    create_playlist,
    get_playlist_id,
    update_playlist,
    errors,
)  # For creating and updating a playlist


# A named tuple representing a user in the users.csv table
class User(NamedTuple):
    name: str  # Example: "abosh"
    email: str  # Example: "abosh@email.com"
    last_fm_username: str  # Example: "yayabosh"
    thresholds: List[int]  # Example: 100
    moniker: str  # Example: "Abosh Has", so the Spotify playlist will be named "Songs {Abosh Has} Listened To 100+ Times"


# Get users from users.csv and create a list of User objects
users = []
with open("tables/users.csv", newline="") as f:
    # Parse each line in users.csv, ignoring lines that start with a #
    reader = csv.DictReader(row for row in f if not row.startswith("#"))
    for row in reader:
        # Create a User object for each row in `users.csv` and add it to the users list
        thresholds = row["thresholds"].split(",")
        users.append(
            User(
                row["name"],
                row["email"],
                row["last_fm_username"],
                sorted([int(threshold) for threshold in thresholds], reverse=True),
                row["moniker"],
            )
        )

# For each user in the users list, get their top tracks (tracks above their
# threshold) from Last.fm and create a playlist for them in Spotify
for user in users:
    # A mapping from the playlist ID for a user's threshold to the songs in the
    # playlist.
    # Example: {[id: 1]: (threshold: 100, [song1, song2, song3]),
    #           [id: 2]: (threshold: 200, [song1, song2, song3])}
    playlist_id_map = {}
    # Iterate through each threshold for the user and create or update a playlist
    # for them
    for threshold in user.thresholds:
        # Get the tracks of the user played more than the given threshold
        get_tracks_above_threshold(user, threshold)
        # Get the playlist ID for the user's playlist, if it exists
        playlist_id = get_playlist_id(user, threshold)
        # If the playlist doesn't exist, create it
        if playlist_id is None:
            playlist_id = create_playlist(user, threshold)

        # Update the playlist with the the tracks played more than the given
        # threshold
        new_tracks = update_playlist(playlist_id)

        # Map the playlist ID to a tuple containing the threshold and the songs
        # in the playlist. This will be used when sending an email to the user.
        playlist_id_map[playlist_id] = (threshold, new_tracks)

    # Send an update email to the user
    send_email(user, playlist_id_map, errors)
