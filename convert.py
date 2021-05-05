from SpotifyScraper.scraper import Scraper, Request
from youtubesearchpython import VideosSearch
import pprint
from datetime import datetime

pp = pprint.PrettyPrinter(indent=4)
URL = "https://open.spotify.com/playlist/5lhfU2WFPlp9KDA0F7yuAk?si=7392b181f4a04cb8&nd=1"
FMT = '%M:%S'
FMT2 = '%H:%M:%S'

def get_spotify_playlist(url):
    '''Use SpotifyScraper to get a list of tracks in a spotify playlist.'''
    request = Request().request()
    playlist_info = Scraper(session=request).get_playlist_url_info(url=URL)
    return playlist_info['tracks_list']

def get_youtube_video_list(spotify_playlist):
    '''Turn spotify playlist into YouTube video list.'''
    playlist = []
    unfound = []
    videos = 'https://www.youtube.com/watch_videos?video_ids='
    for track in spotify_playlist:
        if track['ERROR'] is not None:
            unfound.append(track['track_name'])
            continue
        search = track['track_name'] + track['track_singer']
        search += track['track_album'] if track['track_album'] != track['track_name'] else ''
        videosSearch = VideosSearch(track['track_name'] + track['track_singer'], limit=3)
        results = videosSearch.result()['result']
        duration = track['duration']
        if duration is None:
            playlist.append({
                            'track_name': track['track_name'],
                            'track_singer': track['track_singer'], 
                            'track_album': track['track_album'], 
                            'best_url': results[0]['link'].replace('watch?v=', 'embed/')
                        })
            videos += results[0]['link'].replace('https://www.youtube.com/watch?v=', '') + ','
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
                if r_dur is None:
                    continue
                if len(r_dur.split(':')) == 2:
                    r_dur = datetime.strptime(r_dur, FMT)
                else:
                    r_dur = datetime.strptime(r_dur, FMT2)
                delta = abs(duration - r_dur)
                if best is None or delta < duration_difference:
                    best = result['link']
                    duration_difference = delta
        playlist.append({
                            'track_name': track['track_name'],
                            'track_singer': track['track_singer'], 
                            'track_album': track['track_album'], 
                            'best_url': best.replace('watch?v=', 'embed/')
                        })
        videos += best.replace('https://www.youtube.com/watch?v=', '') + ','
    return (playlist, unfound, videos[:-1])

def convert_spotify_to_youtube(url):
    '''Convert a SpotifyPlaylist into a YouTube video url list.'''
    playlist, not_found, videos = get_youtube_video_list(get_spotify_playlist(url))
    return {'playlist': playlist, 'not_found': not_found, 'videos': videos}

if __name__ == '__main__':
    pp.pprint(convert_spotify_to_youtube(URL))
