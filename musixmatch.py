import requests
import re
import os

URL = 'https://apic-desktop.musixmatch.com/ws/1.1/macro.subtitles.get'
SUBTITLES_REGEX = re.compile("\\[(\\d+):(\\d+).(\\d+)\\] (.+)\n")

memory_cache = {}

def get_lyrics(artist, track):

    # Check if it is in memory
    if (artist, track) in memory_cache:
        return memory_cache[(artist, track)]

    # Check if it is stored in a file
    sanitized_name = "{}-{}.lrc".format(artist, track).replace('/','-')
    if os.path.exists(os.path.join("/usr/share/lyrics", sanitized_name)):
        with open(os.path.join("/usr/share/lyrics", sanitized_name), "r") as f:
            raw_subtitles = f.read()
    else:
        request = requests.get(url=URL, params={
            'format': 'json',
            'q_track': track,
            'q_artist': artist,
            'user_language': 'en',
            'f_subtitle_length': '0',
            'f_subtitle_length_max_deviation': '0',
            'subtitle_format': 'lrc',
            'app_id': 'web-desktop-app-v1.0',
            'guid': 'e08e6c63-edd1-4207-86dc-d350cdf7f4bc',
            'usertoken': '1710144894f79b194e5a5866d9e084d48f227d257dcd8438261277',
        })
        raw_subtitles = (request.json()['message']['body']['macro_calls']
                                        ['track.subtitles.get']['message']
                                        ['body']['subtitle_list'][0]['subtitle']
                                        ['subtitle_body'])
        with open(os.path.join("/usr/share/lyrics", sanitized_name), "w") as f:
            f.write(raw_subtitles)
    captures = SUBTITLES_REGEX.findall(raw_subtitles)
    time_fixed = map(lambda x: (float(x[0])*60 + float(x[1]) + float(x[2])/100, x[3]), captures)
    final = list(time_fixed)
    final.reverse()
    memory_cache[(artist, track)] = final
    return final


if __name__ == "__main__":
    print(get_lyrics("La Mosca en Tu Pared", "Vetusta Morla"))
