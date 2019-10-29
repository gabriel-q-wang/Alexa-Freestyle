# HackGT2019 "Alexa Freestyle"

Team Old Town Code's project submission to Georgia Tech's annual hackathon "HackGT."

This project uses Amazon's Alexa custom skills to generate new songs based on a band's existing lyrics.

Uses Amazon's Alexa service to query the user for which band they wish to generate songs for.

An Amazon Web Service "Lambda" service is then pinged on user input. The Lambda handles any exceptions and calls the backend server to get the new lyrics for the Alexa to recite.

An Amazon Web Service "Elastic Compute Cloud" service, which is running a Flask backend server, is called to access the data the user is requesting. The flask server uses the band input to query a lyric API to get a band data set. Then this set of lyrics is used to train a machine learning model which is used to generate new lyrics. If a model has already been trained, the cached model will be used instead.

Future work involves overlaying these lyrics ontop of generated music, and playing that music over an Alexa.
