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
    ): "323ujVhfSg16TlRK0PB5JY",
    (
        "S.II.S (Soul To Soul)",
        "S.E.S.",
    ): "5jM2ITcV8idbVEjhgm52Dd",
    ("BRASILIAN SKIES", "高中正義"): "3bMc9oRaUWnojCrYTUXXcQ",
    ("Disrespectful", "21 Savage, Offset & Metro Boomin"): "3oxCefEI6Tc6Z6t20J4IvH",
    ("Real Friends", "Kanye West"): "66Q3fAmSX5eHamgbKa9alP",
    ("aisatsana [102]", "Aphex Twin"): "3ESsjKqrj3M79I8sSZieK3",
    ("All the Sudden", "Lil Pump"): "3cj95iGe8aqvL5iGl6o0R9",
    ("No Security", "Skepta"): "5gm3fp5ymJlj73v03vO8h8",
    ("Otis", "JAY-Z"): "0nLcWJB4ir9430ulKxZZhV",
    ("Gin N Juice (feat. Dat Nigga Daz)", "Snoop Dogg"): "7sPt2cfrg7DrVP52zfvS1i",
    ("L.E.S.", "Childish Gambino"): "0YsGMHid6sFq5PcToe3JZE",
    ("Gotta Have It", "JAY-Z"): "6JFLZH9vCzgqnUToBdiHQb",
    ("Outside Today", "YoungBoy Never Broke Again"): "3sA7HKGzcKTVscdiTCrWpX",
    ("Stop It", "FISHER"): "4qetR2UUyBeUrJ9DbYrpVQ",
    ("GUMMO", "6ix9ine"): "4HbiCvH1R7mVOJ7KY7JQBD",
    ("My Shadow", "Promiseland"): "1kHY05OYNqmkQmeq02t36X",
    ("난로 마냥 Question Mark", "Suzy"): "32nk0zso1X9pWUxxKM03pV",
    ("Insecure", "BILLY BUEFFER"): "1jxGu8r85Wj4VxfMcsfNBe",
    ("Tell Me", "Era"): "0WUEI3wb6ei1gRvCJChfxA",
    ("alexandria - slowed", "myclownshoes"): "3gCUAa67kcVxX7Mt24ZPhN",
    ("4:38am (feat. Barrie)", "Ford."): "778rI4lJeJKKy34mAeq4KA",
}
