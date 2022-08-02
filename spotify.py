import spotipy
import csv
from googletrans import Translator
from thefuzz import fuzz
from literal_matches import literal_matches
from secrets import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_USERNAME

SCOPE = "playlist-modify-public"

translator = Translator()


token = spotipy.util.prompt_for_user_token(
    SPOTIFY_USERNAME,
    SCOPE,
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri="http://localhost/",
)
sp = spotipy.Spotify(auth=token)


def get_playlist_id(user):
    playlist_name = f"Songs {user.moniker} Played {user.threshold}+ Times"
    playlists = sp.user_playlists(SPOTIFY_USERNAME)["items"]
    for playlist in playlists:
        if playlist["name"] == playlist_name:
            return playlist["id"]

    return None


def create_playlist(user):
    playlist_name = f"Songs {user.moniker} Played {user.threshold}+ Times"
    playlist_description = f"This playlist auto-updates w data from last.fm. \
    Go to github.com/yayabosh/your-greatest-hits to make ur own playlist!"

    sp.user_playlist_create(
        SPOTIFY_USERNAME, name=playlist_name, description=playlist_description
    )
    return get_playlist_id(user)


def get_track_id(song, artist):
    if (song, artist) in literal_matches:
        return literal_matches[(song, artist)]

    results = sp.search(q=f"{song} {artist}", limit=5, type="track")

    if results["tracks"]["total"] == 0:
        raise RuntimeError(
            f"😐 Error: Spotify couldn't find {song} by {artist}. Stop pirating music! 😐"
        )

    for item in results["tracks"]["items"]:
        if (
            fuzz.partial_ratio(item["artists"][0]["name"].lower(), artist.lower()) > 90
            and fuzz.partial_ratio(item["name"].lower(), song.lower()) > 90
        ):
            return item["id"]

    raise RuntimeError(f"🧐 Error: not a close enough match for {song} by {artist} 🧐")


def translate_artist(artist):
    detection = translator.detect(artist)
    if detection.lang == "en":
        return artist

    if isinstance(detection.lang, list):
        for lang, conf in zip(detection.lang, detection.confidence):
            if conf >= 0.5:
                return translator.translate(artist, src=lang, dest="en").text

        return artist

    if detection.confidence >= 0.5:
        return translator.translate(artist, src=detection.lang, dest="en").text

    return artist


def get_track_ids():
    track_ids = []
    with open("tables/songs.csv", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            song = row["song"]
            artist = row["artist"]
            track_id = ""
            try:
                track_id = get_track_id(song, artist)
                track_ids.append(track_id)
            except RuntimeError as e:
                try:
                    track_id = get_track_id(song, translate_artist(artist))
                    track_ids.append(track_id)
                except RuntimeError:
                    print(str(e))

    return track_ids


def update_playlist(playlist_id):
    track_ids = get_track_ids()
    if len(track_ids) <= 100:
        sp.user_playlist_replace_tracks(SPOTIFY_USERNAME, playlist_id, track_ids)
        return

    for i in range(0, len(track_ids), 100):
        sp.user_playlist_remove_all_occurrences_of_tracks(
            SPOTIFY_USERNAME, playlist_id, track_ids[i : i + 100]
        )

    for i in range(0, len(track_ids), 100):
        sp.user_playlist_add_tracks(
            SPOTIFY_USERNAME, playlist_id, track_ids[i : i + 100]
        )
