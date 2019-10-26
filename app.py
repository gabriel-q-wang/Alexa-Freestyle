import sys
import json
import os
import requests
import lyric_generator

def main():
    print('Please enter an artist\'s name: ')
    artist_name = input()
    lyric_generator.get_lyrics_api(artist_name)


main()
