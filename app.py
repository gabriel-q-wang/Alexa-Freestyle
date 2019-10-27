import sys
import json
import os
import requests
import lyric_generator
from textgenrnn import textgenrnn

def main():
    print('Please enter an artist\'s name: ')
    artist_name = input()
    lyric_list = lyric_generator.get_lyrics_api(artist_name)
    artist_name = artist_name.replace(' ', '-')
    print(artist_name)
    if os.path.exists(artist_name + '.hdf5'):
        textgen = textgenrnn('textgenrnn_weights.hdf5')
        textgen.generate_samples()
    else:
        lyric_generator.train_model(lyric_list, artist_name)


main()
