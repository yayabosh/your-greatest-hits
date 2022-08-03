import csv  # For parsing `tables/users.csv``
import logging
from typing import NamedTuple  # For creating a named tuple representing a user

from last_fm import get_top_tracks  # For getting the top tracks for a user
from spotify import (
    create_playlist,
    get_playlist_id,
    update_playlist,
)  # For creating and updating a playlist

# A named tuple representing a user in the `users.csv` table
class User(NamedTuple):
    name: str  # Example: "abosh"
    last_fm_username: str  # Example: "yayabosh"
    threshold: int  # Example: 100
    moniker: str  # Example: "Abosh Has", so the Spotify playlist will be named "Songs {Abosh Has} Listened To 100+ Times"


def setup_logging():
    logging.basicConfig(filename="greatest_hits.log", level=logging.INFO)
    logging.basicConfig(
        filename="",
        format="%(asctime)s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.INFO,
    )


def main():
    setup_logging()

    logging.info("Starting!")
    # Get users from users.csv and create a list of User objects
    users = []
    with open("tables/users.csv", newline="") as f:
        # Parse each line in `users.csv`, ignoring lines that start with a #
        reader = csv.DictReader(row for row in f if not row.startswith("#"))
        for row in reader:
            # Create a User object for each row in `users.csv` and add it to the users list
            users.append(
                User(
                    row["name"],
                    row["last_fm_username"],
                    int(row["threshold"]),
                    row["moniker"],
                )
            )

    # For each user in the users list, get their top tracks (tracks above their
    # threshold) from Last.fm and create a playlist for them in Spotify
    for user in users:
        logging.info(f"Starting for {user.name}.")
        # Get the top tracks for the user
        get_top_tracks(user)
        # Get the playlist ID for the user's playlist, if it exists
        playlist_id = get_playlist_id(user)
        # If the playlist doesn't exist, create it
        if playlist_id is None:
            playlist_id = create_playlist(user)

        # Update the playlist with the top tracks for the user
        update_playlist(playlist_id)

    logging.info("Finished!")


if __name__ == "__main__":
    main()
