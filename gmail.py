import datetime  # For getting the current date

# For sending emails
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from secret import GMAIL_APP_PASSWORD, GMAIL_SENDER, GMAIL_PERSONAL_EMAIL

# Get today's date
today = datetime.datetime.now()


def italicize(text):
    return f"<em>{text}</em>"


def underline(text):
    return f"<u>{text}</u>"


def bold(text):
    return f"<b>{text}</b>"


def strikethrough(text):
    return f"<s>{text}</s>"


def link(text, url):
    return f'<a href="{url}">{text}</a>'


def line_break():
    return "<br>"


def playlist_id_to_link(playlist_id):
    return f"https://open.spotify.com/playlist/{playlist_id}"


# Sends an email to the user containing an update for all the user's playlists.
def send_email(user, playlist_id_map, errors):
    print(f"📤 Sending email to {user.name} at {user.email}...")

    sender_email = GMAIL_SENDER
    receiver_email = user.email
    password = GMAIL_APP_PASSWORD

    message = MIMEMultipart("alternative")
    message[
        "Subject"
    ] = f"Your Greatest Hits - {today.strftime('%B')} {today.strftime('%Y')}"
    message["From"] = f"Abosh Upadhyaya <{sender_email}>"
    message["To"] = receiver_email

    MULTIPLE_PLAYLISTS = len(playlist_id_map) > 1
    PLURAL_PLAYLISTS = "playlists" if MULTIPLE_PLAYLISTS else "playlist"
    plain_text = f"""
    """
    months_since = 3
    months_updated = months_since - user.month_joined
    html = f"""
<html>
  <body>
    <p>Hey {user.name},</p>
    <p>
      This is a new project I’m working on. It creates Spotify playlists for you based on your listening history.
      Specifically, it creates a playlist for songs you’ve played over a certain threshold amount of times.
    </p>
    <p>
      There’s currently {bold("26")} people (+6 this past month!) I’m debuting this with. Hopefully, I’ll be able to get more people on board soon.
      Let your friends or family know if you think this is cool! All I need is their Spotify username, Last.fm username, and email address.
      I promise I’ll never spam anyone. I’ll only send emails like this one once a month.
    </p>
    <p>
      The cool thing about this project is that it’s completely automated, and it’ll last forever.
      This is the third one ever, and see you next month!
    </p>
    <p>
      ---------------------------------
    </p>
    <p>Your monthly update for {bold("Your Greatest Hits")} is ready! 🥳</p>
    <p>
      You currently have {bold(f"{len(playlist_id_map)} {PLURAL_PLAYLISTS}")}
      tracking songs. Want to add another playlist with a new threshold? Just
      reply to this email!
    </p>
    <p>
      🎶 {bold(underline("Update Summary"))}
      {line_break()}
      {get_update_summary(playlist_id_map)}
    </p>
    {line_break()}
    <p>
      😵 {bold(f"{underline('Errors')} — {italicize('Is it too late now to say sorry?')}")}
      {line_break()}
      {get_non_added_songs(errors, PLURAL_PLAYLISTS)}
    </p>
    <p>
      😔 {bold(f"Error #1: {italicize('I listened to a song but it wasn’t added.')}")}
      {line_break()}
      This usually happens for one of the following reasons:
      {line_break()}
      1. {bold("You listen to foreign music")} (good for you!) which Spotify’s 
         catalog doesn't have, or has but under a different song or artist name.
         This usually happens since Spotify likes to translate artist names to
         English but Last.fm doesn’t.
      {line_break()}
      2. {bold("You listen to pirated music")} ({strikethrough("good for you!")})
         that isn’t on Spotify.
      {line_break()}
      3. {bold("You listen to music through YouTube, SoundCloud, or something else that formats the song title or artist name differently than Spotify.")}
      {line_break()}
      4. {bold("I messed up.")} If a song really is on Spotify but it couldn’t
         be found, for any reason, let me know and I’ll fix this for you!
    </p>
    <p>
      🤨 {bold(f"Error #2: {italicize('A song that I didn’t listen to got added.')}")}
      {line_break()}
      If there’s any songs in your playlist that are different from the song you
      listened to, for any of the following reasons, let me know and I’ll try
      and get it fixed.
      {line_break()}
      1. {bold("A song got added that you didn't listen to that many times.")}
         Like “{bold("Meh")}” by {bold("Playboi Carti")} being added when you
         really only listened to “{bold("@ MEH")}” by {bold("Playboi Carti")}.
         It's like a musical homophone! This error usually occurs because the
         Spotify API sucks at searching for songs.
      {line_break()}
      2. {bold("The right song and artist got added, but for the wrong album.")}
         Like “{bold("INDUSTRY BABY")}” by {bold("Lil Nas X")} getting added,
         but off some random {bold("Kidz Bop")} album.
         This error also usually occurs because the Spotify API sucks at searching for
         songs.
      {line_break()}
      3. {bold("The right song and artist got added, but on an album you just don’t like.")}
         Like a song got added from the deluxe or remastered version of an album,
         but you want it to be from the non-deluxe or remastered version. Or you
         just want the album version since you hate looking at the single version's
         album art. This error is just humans being picky, but I love it!
    </p>
    {line_break()}
    <p>
      {bold(f"{bold(underline('Your Time with Your Greatest Hits'))} — {italicize('stats and extras!')}")}
      {line_break()}
      - Your {PLURAL_PLAYLISTS} {"has" if PLURAL_PLAYLISTS == "playlist" else "have"} been updating for {months_updated} {"months" if months_updated > 1 else "month"}!
        {bold("You’ve been here since the beginning")}! ❤️ (This stat will probably
        seem more impressive years down the line.)
      {line_break()}
      - more stats to be added soon...if you have any suggestions, let me know
        😶‍🌫️😶‍🌫️😶‍🌫️...
      {line_break()}
    </p>
    {line_break()}
    <p>
      This is your greatest hits playlist, filled with songs you demonstrably
      are/were obsessed with at some point in your life. It’s updated by your
      listening from {bold("now until the end of time")}.
    </p>
    <p>
      Unfortunately, your playlist must be created by my account (or else I’d
      need to ask for your Spotify username and password), but you can still
      click “{bold("Add to Profile")}” so it shows up on yours.
    </p>
    <p>
      If you have any questions or feedback, please contact me at
      {GMAIL_PERSONAL_EMAIL} or
      {link("read the docs", "https://github.com/yayabosh/your-greatest-hits")}
      (which are in the process of being written).
    </p>
    <p>
      Happy listening,
      {line_break()}
      Abosh
      {line_break()}
      <pre>
 _                             
| |                            
| |__   __ _ _ __  _ __  _   _ 
| '_ \ / _` | '_ \| '_ \| | | |
| | | | (_| | |_) | |_) | |_| |
|_| |_|\__,_| .__/| .__/ \__, |
            | |   | |     __/ |
            |_|   |_|    |___/ 
 _ _     _                     
| (_)   | |                    
| |_ ___| |_ ___ _ __          
| | / __| __/ _ \ '_ \         
| | \__ \ ||  __/ | | |        
|_|_|___/\__\___|_| |_|        
                               
                               
 _                             
(_)                            
 _ _ __   __ _                 
| | '_ \ / _` |                
| | | | | (_| |                
|_|_| |_|\__, |                
          __/ |                
         |___/  
      </pre>               
    </p>
    <p>
      True Fact: this automated email cost me {bold("$1.00")} to send. If you want
      to show your appreciation, please consider paying me this amount 😊 (Feel free
      to exceed this amount as well.) Venmo: @yayabosh
    </p>
    <p>
      I’m just kidding! This project has no budget! At least until my roommate
      realizes he’s the one paying for the AWS server... Ivan don’t read this 😃👍
    </p>
  </body>
</html>
"""

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(plain_text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def get_update_summary(playlist_id_map):
    summary = ""
    for playlist_id, (threshold, new_tracks) in playlist_id_map.items():
        playlist_title = f"Songs You’ve Listened To {threshold}+ Times"
        summary += f"""{bold(link(playlist_title, playlist_id_to_link(playlist_id)))}
                       {line_break()}"""
        summary += f"{get_new_songs(new_tracks)}{line_break()}"

    return summary


def get_new_songs(new_tracks):
    if not new_tracks:
        return f"""😔 {italicize(
          'No new additions this month. Keep listening, and you’ll see more soon!'
        )}{line_break()}"""

    result = f"🔥 {italicize('Woohoo, you’ve got updates!')}{line_break()}"
    result += f"""The following 
                  {'song was' if len(new_tracks) == 1 else 'songs were'} 
                  added:{line_break()}"""
    count = 0
    for (song, artist) in new_tracks:
        if count == 15:
            result += f"and {bold(len(new_tracks) - count)} more...{line_break()}"
            break

        result += f"- “{bold(song)}” by {bold(artist)}{line_break()}"
        count += 1

    return result


def get_non_added_songs(errors, PLURAL_PLAYLIST):
    if not errors:
        return f"""This month, {bold('all songs were added successfully!')}
                  That means you shouldn’t be missing any songs in your playlist.
                  But {bold('you should still check your playlist for songs that shouldn’t be there')}.
                  Keep reading this section for more info."""

    PLURAL_SONG = "this song" if len(errors) == 1 else "these songs"
    result = f"""☹️ This month, {PLURAL_SONG} couldn’t be added to your
                 {PLURAL_PLAYLIST}:{line_break()}"""
    for (song, artist) in errors:
        result += f"- “{bold(song)}” by {bold(artist)}{line_break()}"

    result += f"{line_break()}Keep reading this section for info on why that might have happened."
    return result
