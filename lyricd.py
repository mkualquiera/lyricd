#!/usr/bin/env python3

import spotify
import musixmatch
import time
import os

OFFSET = 0.9

while True:
    author, track, progress = spotify.get_playback()
    if track != None:
        try:
            lyrics = musixmatch.get_lyrics(author, track)
            to_show = next((x[1] for x in lyrics if x[0] < progress + OFFSET), "")
        except:
            to_show = "Lyrics unavailable"

        with open(os.path.join("/opt/lyricd", "lyrics.txt"), "w") as f:
            f.write(to_show)
        with open(os.path.join("/opt/lyricd", "playback.txt"), "w") as f:
            f.write("Playing: {} - {}".format(author, track))

    time.sleep(1)

