'''
    astronaut_webapp
    Etienne Richart
'''
import sys
import os
import flask
import json
from convert import convert_spotify_to_youtube
import pprint

pp = pprint.PrettyPrinter(indent=4)
api = flask.Blueprint('api', __name__)

########### The API endpoints ###########
@api.route('/help/')
def get_help():
    '''Returns an HTML page with the API Documentation and Database Schema'''
    return flask.render_template('help.html')

@api.route('/convert/<path:url>')
def convert(url):
    x = convert_spotify_to_youtube(url)
    pp.pprint(x)
    return json.dumps(x)