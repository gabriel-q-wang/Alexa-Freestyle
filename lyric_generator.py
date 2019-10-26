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
                lyrics = lyrics.replace('\'', '')
                lyrics = lyrics.replace('\\n', ' ')
                lyrics = lyrics.replace('\n', ' ')
                lyrics = lyrics.replace('\\', ' ')
                lyrics_list.append(lyrics)

        print(lyrics_list)
        return lyrics_list
    except:
        print("Error")

def train_model(lyric_list):
    textgen = textgenrnn()
    print(textgen.train_on_texts(lyric_list, num_epochs=10,  gen_epochs=2))
    '''model_cfg = {
        'rnn_size': 500,
        'rnn_layers': 12,
        'rnn_bidirectional': True,
        'max_length': 15,
        'max_words': 10000,
        'dim_embeddings': 100,
        'word_level': False,
    }

    train_cfg = {
        'line_delimited': True,
        'num_epochs': 100,
        'gen_epochs': 25,
        'batch_size': 750,
        'train_size': 0.8,
        'dropout': 0.0,
        'max_gen_length': 300,
        'validation': True,
        'is_csv': False
    }

    uploaded = files.upload()
    all_files = [(name, os.path.getmtime(name)) for name in os.listdir()]
    latest_file = sorted(all_files, key=lambda x: -x[1])[0][0]

    model_name = '500nds_12Lrs_100epchs_Model'
    textgen = textgenrnn(name=model_name)

    train_function = textgen.train_from_file if train_cfg['line_delimited'] else textgen.train_from_largetext_file

    train_function(
        file_path=latest_file,
        new_model=True,
        num_epochs=train_cfg['num_epochs'],
        gen_epochs=train_cfg['gen_epochs'],
        batch_size=train_cfg['batch_size'],
        train_size=train_cfg['train_size'],
        dropout=train_cfg['dropout'],
        max_gen_length=train_cfg['max_gen_length'],
        validation=train_cfg['validation'],
        is_csv=train_cfg['is_csv'],
        rnn_layers=model_cfg['rnn_layers'],
        rnn_size=model_cfg['rnn_size'],
        rnn_bidirectional=model_cfg['rnn_bidirectional'],
        max_length=model_cfg['max_length'],
        dim_embeddings=model_cfg['dim_embeddings'],
        word_level=model_cfg['word_level'])

        print(textgen.model.summary())

    files.download('{}_weights.hdf5'.format(model_name))
    files.download('{}_vocab.json'.format(model_name))
    files.download('{}_config.json'.format(model_name))

    textgen = textgenrnn(weights_path='6layers30EpochsModel_weights.hdf5',
                           vocab_path='6layers30EpochsModel_vocab.json',
                           config_path='6layers30EpochsModel_config.json')

    generated_characters = 300

    textgen.generate_samples(300)
    textgen.generate_to_file('lyrics.txt', 300)'''
