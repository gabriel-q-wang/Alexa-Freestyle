import sys
import json
import os
import requests
from textgenrnn import textgenrnn
from musixmatch import Musixmatch
from __future__ import print_function
import numpy

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
def get_audio_response(artist_name):
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    session_attributes = {}
    card_title = "Test"

    speech_output = main(artist_name)
    reprompt_text = "Ok, give me a second to get some inspiration from " + artist_name
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Opening Auto tune. DJ Alexa is in the house! What do you want to hear?"
    reprompt_text = "DJ Alexa is in the house! What do you want to hear?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thanks for listening to Auto tune!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass

def on_launch(launch_request, session):
    # Called when the user launches the skill without specifying what they want
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "AutoTuneIntern":
        artist_name = intent['slots']['band']['value']
        return get_audio_response(artist_name)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
#------------------------------------------------------------------------------
def get_lyrics_api(artist_name):
    musixmatch_key = ''
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
                lyrics = lyrics.replace('\\n', '.')
                lyrics = lyrics.replace('\n', '.')
                final_verse_list.append(lyrics)

        return final_verse_list
    except:
        print("Error")

def train_model(lyric_list, artist_name):
    textgen = textgenrnn()
    print(textgen.train_on_texts(lyric_list, num_epochs=20,  gen_epochs=1))
    #textgen.save(artist_name + '.hdf5')

def main(artist_name):
    lyric_list = get_lyrics_api(artist_name)
    artist_name = artist_name.replace(' ', '-')
    train_model(lyric_list, artist_name)
    return textgen.generate(1)
    '''if os.path.exists(artist_name + '.hdf5'):
        textgen = textgenrnn('textgenrnn_weights.hdf5')
        textgen.generate_samples()
    else:
        train_model(lyric_list, artist_name)'''
