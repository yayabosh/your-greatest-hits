import csv  # For parsing tables/songs.csv

import spotipy  
from googletrans import Translator
from thefuzz import fuzz

from literal_matches import literal_matches
from secret import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_USERNAME

SCOPE = "playlist-modify-public"

translator = Translator()

errors = {}

token = spotipy.util.prompt_for_user_token(
    SPOTIFY_USERNAME,
    SCOPE,
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri="http://localhost/",
)
sp = spotipy.Spotify(auth=token)


def get_playlist_id(user, threshold):
    playlist_name = f"Songs {user.moniker} Played {threshold}+ Times"
    playlists = sp.user_playlists(SPOTIFY_USERNAME)["items"]
    for playlist in playlists:
        if playlist["name"] == playlist_name:
            return playlist["id"]

    return None


def create_playlist(user, threshold):
    playlist_name = f"Songs {user.moniker} Played {threshold}+ Times"
    playlist_description = f"This playlist auto-updates w data from last.fm. Go to github.com/yayabosh/your-greatest-hits to make ur own playlist!"

    sp.user_playlist_create(
        SPOTIFY_USERNAME, name=playlist_name, description=playlist_description
    )
    return get_playlist_id(user, threshold)


def get_track_id(song, artist):
    if (song, artist) in literal_matches:
        return literal_matches[(song, artist)]

    results = sp.search(q=f"{song} {artist}", limit=5, type="track")

    if results["tracks"]["total"] == 0:
        errors[(song, artist)] = "not_found"
        raise RuntimeError(
            f"😐 Error: Spotify couldn't find {song} by {artist}. Stop pirating music! 😐"
        )

    for item in results["tracks"]["items"]:
        if (
            fuzz.partial_ratio(item["artists"][0]["name"].lower(), artist.lower()) > 90
            and fuzz.partial_ratio(item["name"].lower(), song.lower()) > 90
        ):
            return item["id"]

    errors[(song, artist)] = "not_close_enough_match"
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


def get_current_tracks():
    track_ids_to_songs = {}
    with open("tables/songs.csv", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            song = row["song"]
            artist = row["artist"]
            track_id = None
            try:
                track_id = get_track_id(song, artist)
            except RuntimeError as e:
                try:
                    track_id = get_track_id(song, translate_artist(artist))
                except RuntimeError:
                    print(str(e))

            if track_id is not None:
                track_ids_to_songs[track_id] = (song, artist)

    return track_ids_to_songs


def get_old_track_ids(playlist_id):
    old_track_ids = set()
    results = sp.user_playlist_tracks(SPOTIFY_USERNAME, playlist_id)
    tracks = results["items"]
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    for track in tracks:
        old_track_ids.add(track["track"]["id"])

    return old_track_ids


def update_playlist(playlist_id):
    current_tracks = get_current_tracks()

    current_track_ids = current_tracks.keys()
    old_track_ids = get_old_track_ids(playlist_id)

    difference = set(current_track_ids) - old_track_ids
    if len(difference) == 0:
        return []

    new_track_ids = [
        track_id for track_id in current_track_ids if track_id in difference
    ]
    for i in range(0, len(new_track_ids), 100):
        sp.user_playlist_add_tracks(
            SPOTIFY_USERNAME, playlist_id, new_track_ids[i : i + 100]
        )

    return [current_tracks[track_id] for track_id in difference]
