'''
    astronaut_webapp
    Etienne Richart
'''
import sys
import os
import flask
import json

api = flask.Blueprint('api', __name__)

########### The API endpoints ###########
@api.route('/help/')
def get_help():
    '''Returns an HTML page with the API Documentation and Database Schema'''
    return flask.render_template('help.html')

    
