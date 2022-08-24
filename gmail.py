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
    html = f"""
<html>
  <body>
    <p>Hey {user.name},</p>
    <p>Your monthly update for {bold("Your Greatest Hits")} is ready! 🥳</p>
    <p>
      You currently have {bold(f"{len(playlist_id_map)} {PLURAL_PLAYLISTS}")}
      tracking songs. Want to add another playlist with a new threshold? Just
      reply to this email!
    </p>
    <p>
      🎶 {bold(underline("Update Summary"))}
      {line_break()}
      {bold(link("Songs You’ve Listened To 100+ Times", 
      ""))}
      {line_break()}
      Woohoo, you’ve got updates!" 🔥
      {line_break()}
      The following songs were added:
      {line_break()}
      - “{bold("Famous")}” by {bold("Kanye West")}
      {line_break()}
      - “{bold("Massive")}” by {bold("Drake")}
    </p>
    <p>
      {bold(link("Songs You’ve Listened To 60+ Times", 
      ""))}
      {line_break()}
      No new additions this month. 😔 But there's always next month!
      {line_break()}
    </p>
    <p>
      🙋‍♀️ {bold(underline("Errors"))} - {italicize("Is it too late now to say sorry?")}
      {line_break()}
      😔 {bold("I listened to a song but it wasn’t added.")}
      {line_break()}
      This month, these songs couldn’t be added to your {PLURAL_PLAYLISTS}:
      {line_break()}
      - “{bold("Nice Guys")}” by {bold("Chester See, Kevjumba & Ryan Higa")}
    </p>
    <p>
      Spotify usually can’t find songs for one of these reasons:
      {line_break()}
      1. {bold("You listen to foreign music")} (good for you!) which Spotify’s 
         catalog doesn't have, or has but under a different song or artist name.
         This usually happens since Spotify likes to translate artist names to
         English but Last.fm doesn’t.
      {line_break()}
      2. {bold("You listen to pirated music")} ({strikethrough("good for you!")}).
      {line_break()}
      3. {bold("I messed up.")} If a song really is on Spotify but it couldn’t
         be found, let me know and I’ll fix this for you!
    </p>
    <p>
      🤨 {bold("A song that I didn’t listen to got added.")}
      {line_break()}
      If there’s any songs in your playlist that are different from the song you
      listened to, for any of the following reasons, let me know and I’ll try
      and get it fixed.
      {line_break()}
      1. {bold("A song got added that you didn't listen to that many times.")}
         Like “{bold("Meh")}” by {bold("Playboi Carti")} being added when you
         really only listened to “{bold("@ MEH")}” by {bold("Playboi Carti")}.
      {line_break()}
      2. {bold("The right song and artist got added, but for the wrong album.")}
         Like “{bold("INDUSTRY BABY")}” by {bold("Lil Nas X")} getting added,
         but off some random {bold("Kidz Bop")} album.
      {line_break()}
      3. {bold("The right song and artist got added, but on an album you just don’t like.")}
         Like a song got added from the deluxe or remastered version of an album,
         but you want it to be from the non-deluxe or remastered version.
    </p>
    <p>
      Finally, some extra stats about your time with Your Greatest Hits:
      {line_break()}
      - Your {PLURAL_PLAYLISTS} have been updating for {bold("1 month")}!
        {bold("You’ve been here since the beginning")}! ❤️ (This stat will probably
        seem more impressive years down the line.)
      {line_break()}
      - more stats to be added soon...if you have any suggestions, let me know
        😶‍🌫️😶‍🌫️😶‍🌫️...
      {line_break()}
    </p>
    <p>
      This is your greatest hits playlist, filled with songs you demonstrably
      are/were obsessed with at some point in your life. It’s updated by your
      listening, I’m just a middleman. Unfortunately, your playlist is created
      by my account (or else I’d need to ask for your Spotify username and
      password), but you can still click “{bold("Add to Profile")}” so it shows
      up on yours.
    </p>
    <p>
      If you have any questions, please contact me at {GMAIL_PERSONAL_EMAIL} or
      {link("read the docs", "https://github.com/yayabosh/your-greatest-hits")}.
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
