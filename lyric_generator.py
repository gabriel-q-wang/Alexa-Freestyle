import config
import sys
import json
import os
import requests
import numpy as np
import pandas as pd
from textgenrnn import textgenrnn
from musixmatch import Musixmatch

def get_lyrics_api(artist_name):
    musixmatch_key = config.MUSIXMATCH_KEY
    musixmatch = Musixmatch(musixmatch_key)
    lyrics_list = []
    final_verse_list = []
    try:
        artists_json = musixmatch.artist_search(q_artist=artist_name, page_size=1, page=1, f_artist_id="", f_artist_mbid="")
        artist_id = artists_json['message']['body']['artist_list'][0]['artist']['artist_id']

        albums_json = musixmatch.artist_albums_get(artist_id=artist_id, page_size=5, page=1, s_release_date='desc', g_album_name="")
        albums_list = albums_json['message']['body']['album_list']
        for album in albums_list:
            albums_id = album['album']['album_id']

            tracks_json = musixmatch.album_tracks_get(album_id=albums_id,f_has_lyrics=True,page_size=20, page=1,album_mbid='')
            tracks_list = tracks_json['message']['body']['track_list']

            for track in tracks_list:
                tracks_id = track['track']['track_id']

                lyrics_json = musixmatch.track_lyrics_get(tracks_id)
                lyrics = lyrics_json['message']['body']['lyrics']['lyrics_body']
                sep = '*******'
                lyrics = lyrics.split(sep, 1)[0]
                lyrics = lyrics.replace('\\', ' ')
                lyrics = lyrics.replace('\"', ' ')
                lyrics = lyrics.replace('\\n', ',')
                lyrics = lyrics.replace('\n', ',')
                #lyrics = lyrics.replace('...', ',')
                #lyrics = lyrics.replace('?', ' ')
                #lyrics = lyrics.replace('!', ' ')
                final_verse_list.append(lyrics)

        return final_verse_list
    except:
        return None

def train_model(lyric_list, artist_name):
    textgen = textgenrnn()
    textgen.train_on_texts(lyric_list, num_epochs=1,  gen_epochs=1)
    textgen.save(artist_name + '.hdf5')
