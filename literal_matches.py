# Represents hardcoded literal matches for the parser.
# Sometimes Spotify just can’t find a track, finds the wrong one, or Last.fm
# will translate a track or artist name into a different language.
#
# This list is by no means exhaustive, but it’ll get updated as I find more
# cases.
literal_matches = {
    (
        "@ MEH",
        "Playboi Carti",
    ): "5UusfWUMMLEXLMc1ViNZoe",  # Spotify finds "Meh" by Playboi Carti
    (
        "WALK IN THE PARK",
        "Jack Harlow",
    ): "0XOKietGW4PXK4hs4jyfpO",  # Spotify finds the right song, but a different album
    (
        "POPSTAR (feat. Drake)",
        "DJ Khaled",
    ): "1sbEeUY8KsdvgiQi26JBFz",  # Spotify finds the right song, but a different album
    (
        "Woah",
        "Lil Baby",
    ): "4P1GuhD2Su9jjyRDPdbeUf",  # Spotify finds the right song, but a different album
    (
        "Ric Flair Drip (& Metro Boomin)",
        "Offset",
    ): "7sO5G9EABYOXQKNPNiE9NR",  # Spotify can’t find this song since the name was changed
    (
        "Heroes - 1999 Remastered Version",
        "David Bowie",
    ): "7Jh1bpe76CNTCgdgAdBw4Z",  # Spotify can’t find this song
    (
        "童話",
        "光良",
    ): "6NCylXeJcHOI908PjZDFcg",  # Last.fm translates this artist’s name, so Spotify can’t find it
    ("My Boy (Twin Fantasy)", "Car Seat Headrest"): "4zQXB3sZrpT2gA3rgYl3sY",
    (
        "Prayer in C - Robin Schulz Radio Edit",
        "Lilly Wood & The Prick",
    ): "5fnA9mkIfScSqHIpeDyvck",
    (
        "The Birds Part 1",
        "The Weeknd",
    ): "323ujVhfSg16TlRK0PB5JY"
}
