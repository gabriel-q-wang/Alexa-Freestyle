import config
import sys
import json
import os
import requests
import numpy as np
import pandas as pd
#from textgenrnn import textgenrnn
from musixmatch import Musixmatch

def get_lyrics_api():
    musixmatch_key = config.MUSIXMATCH_KEY
    musixmatch = Musixmatch(musixmatch_key)
    lyrics = musixmatch.matcher_lyrics_get('Sexy and I know it', 'LMFAO')
    print(lyrics)
    images = []
    '''try:
        image = None
        session = requests.Session()
        # these are sent along for all requests
        session.headers['X-IG-API-KEY'] = API_KEY
        url = 'https://images-api.nasa.gov/search?q=%s' % query
        response = requests.get(url).json()
        collection = response.get('collection')
        items = collection.get('items')
        top_ten = items[:10]

        for item in top_ten:
            links = item.get('links')
            data = item.get('data')
            image = links[0].get('href')
            images.append(image)

        return images
    except:
        print("Error Occurred")
        return images'''

def train_model():
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
