import requests

LAST_FM_API_KEY = "YOUR_LAST_FM_API_KEY"
LAST_FM_SHARED_SECRET = "YOUR_LAST_FM_SHARED_SECRET"

NUM_PAGES = 4


def get_top_tracks(user):
    last_fm_payload = {
        "api_key": LAST_FM_API_KEY,
        "method": "user.getTopTracks",
        "user": user.last_fm_username,
        "format": "json",
    }
    pages = []
    for p in range(1, NUM_PAGES + 1):
        last_fm_payload["page"] = p
        r = requests.get("https://ws.audioscrobbler.com/2.0/", params=last_fm_payload)
        pages.append(r.json()["toptracks"]["track"])

    with open("tables/songs.csv", "w") as f:
        f.write("song,artist\n")
        for page in pages:
            for song in page:
                if int(song["playcount"]) >= user.threshold:
                    f.write(f'"{song["name"]}","{song["artist"]["name"]}"\n')
