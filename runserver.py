# -*- coding: utf-8 -*-

"""
This script runs the AraVecDemo application using a development server.
"""

from os import environ
from AraVecDemo import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    app.secret_key = '!sfg#4skGX!$G356R(@)tu34_'
    app.run(HOST, PORT, debug = True)
