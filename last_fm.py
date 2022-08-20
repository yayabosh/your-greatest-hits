import requests  # For calling the Last.fm API

from secret import LAST_FM_API_KEY

# Number of pages to search through a user's top tracks. This number is
# arbitrary, but it works so far, so I'll update it later.
NUM_PAGES = 4


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
    # Stores all songs in the user's first NUM_PAGES of top tracks.
    pages = []
    # Call the Last.fm API NUM_PAGES times and add the results to pages.
    for p in range(1, NUM_PAGES + 1):
        last_fm_payload["page"] = p
        r = requests.get("https://ws.audioscrobbler.com/2.0/", params=last_fm_payload)
        pages.append(r.json()["toptracks"]["track"])

    # Add all songs played more than the given threshold to songs.csv.
    with open("tables/songs.csv", "w") as f:
        f.write("song,artist\n")
        for page in pages:
            for song in page:
                # This filters songs played less than the given threshold.
                if int(song["playcount"]) >= threshold:
                    f.write(f'"{song["name"]}","{song["artist"]["name"]}"\n')
