import requests  # For calling the Last.fm API

from secret import LAST_FM_API_KEY

# Populates songs.csv with songs played more than the given threshold.
# So if the threshold is 100, songs.csv will contain all songs (and their
# respective artists) played more than 100 times.
def get_tracks_above_threshold(user, threshold):
    # The payload for the Last.fm API call.
    # Read more: https://www.last.fm/api/show/user.getTopTracks
    last_fm_payload = {
        "api_key": LAST_FM_API_KEY,
        "method": "user.getTopTracks",
        "user": user.last_fm_username,
        "format": "json",
    }

    # Clear the songs.csv file
    with open("tables/songs.csv", "w") as f:
        f.write("song,artist\n")

    # Keep calling the Last.fm API while the songs in the last page are played
    # at least threshold number of times. Once we reach a page where the songs
    # are played less than threshold number of times, we can stop.
    page_number = 1  # The page number of the user's scrobbles to retrieve
    while True:
        # Call the Last.fm API and store the result.
        last_fm_payload["page"] = page_number
        r = requests.get("https://ws.audioscrobbler.com/2.0/", params=last_fm_payload)
        page = r.json()["toptracks"]["track"]

        # Append all songs played more than the given threshold to songs.csv.
        with open("tables/songs.csv", "a") as f:
            for song in page:
                # This filters songs played less than the given threshold.
                if int(song["playcount"]) >= threshold:
                    f.write(f'"{song["name"]}","{song["artist"]["name"]}"\n')
                else:
                    # If we reach a page that contains a song played less than
                    # the given threshold, we can stop calling the Last.fm API.
                    return

        page_number += 1
