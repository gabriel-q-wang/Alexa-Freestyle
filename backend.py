from flask_cors import CORS
from flask import Flask
from flask import request

app = Flask(__name__)
CORS(app) #Prevents CORS errors 

@app.route('/')
def index():
    band_name = request.args.get('band')
    return str(band_name) 

if __name__ == '__main__':
    from gevent.pywsgi import WSGIServer
    app.debug = True 
    http_server = WSGIServer(('', 8000), app)
    http_server.serve_forever()
