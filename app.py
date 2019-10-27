import sys
import json
import os
import requests
import lyric_generator
from textgenrnn import textgenrnn

def main():
    artist_name = input('Please enter an artist name: ')
    lyric_list = lyric_generator.get_lyrics_api(artist_name)

    if lyric_list is None:
        return "I'm sorry, I had trouble with your request. Please try again"

    artist_name = artist_name.replace(' ', '-')
    path_name = artist_name + '.hdf5'
    if os.path.exists(path_name):
        textgen = textgenrnn(path_name)
        response = textgen.generate(return_as_list=True)[0]
        return response
    else:
        lyric_generator.train_model(lyric_list, artist_name)
        textgen = textgenrnn(path_name)
        response = textgen.generate(return_as_list=True)[0]
        return response
