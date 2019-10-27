import sys
import json
import os
import requests
import lyric_generator
from textgenrnn import textgenrnn

def main(artist_name):
    print(artist_name)
    lyric_list = lyric_generator.get_lyrics_api(artist_name)
    artist_name = artist_name.replace(' ', '-')
    path_name = artist_name + '.hdf5'
    if os.path.exists(path_name):
        textgen = textgenrnn(path_name)
        print(textgen)
        response = textgen.generate(1)
        print(type(response))
        return response
    else:
        lyric_generator.train_model(lyric_list, artist_name)
        textgen = textgenrnn(path_name)
        print(textgen)
        response = textgen.generate(1)
        print(type(response))
        return response
