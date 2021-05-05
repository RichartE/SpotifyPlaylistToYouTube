from SpotifyScraper.scraper import Scraper, Request
from youtubesearchpython import VideosSearch
import pprint
from datetime import datetime

URL = "https://open.spotify.com/playlist/5lhfU2WFPlp9KDA0F7yuAk?si=7392b181f4a04cb8&nd=1"

request = Request().request()
playlist_info = Scraper(session=request).get_playlist_url_info(url=URL)

pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(playlist_info)
FMT = '%M:%S'
FMT2 = '%H:%M:%S'
playlist = []
for track in playlist_info['tracks_list']:
    if track['ERROR'] is not None:
        continue
    videosSearch = VideosSearch(track['track_name'], limit=3)
    results = videosSearch.result()['result']
    duration = track['duration']
    if duration is None:
        playlist.append((track['track_name'], track['track_singer'], track['track_album'], results[0]['link']))
        continue
    if len(duration.split(':')) == 2:
        duration = datetime.strptime(duration, FMT)
    else:
        duration = datetime.strptime(duration, FMT2)
    duration_difference = None
    best = None
    for result in results:
        if track['duration'] == result['duration']:
            best = result['link']
            break
        else:
            r_dur = result['duration']
            if len(r_dur.split(':')) == 2:
                r_dur = datetime.strptime(r_dur, FMT)
            else:
                r_dur = datetime.strptime(r_dur, FMT2)
            delta = abs(duration - r_dur)
            if best is None or delta < duration_difference:
                best = result['link']
                duration_difference = delta
    playlist.append((track['track_name'], track['track_singer'], track['track_album'], best))


pp.pprint(playlist)