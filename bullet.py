#!/usr/bin/python

import os, argparse, pathlib
from io import BytesIO
from zipfile import ZipFile
import requests

########## Configuration ##########
##### General #####
THIRD_PARTY_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'third_party')

##### Bullet #####
BULLET_VERSION = '2.87'
BULLET_DIRECTORY = os.path.join(THIRD_PARTY_DIR, 'bullet3-' + BULLET_VERSION)

##### Emscripten #####
EMSCRIPTEN_VERSION = '1.37.33'
EMSCRIPTEN_DIRECTORY = os.path.join(THIRD_PARTY_DIR, 'emscripten-' + EMSCRIPTEN_VERSION)

########## Arguments ##########
argument_parser = argparse.ArgumentParser(description='Bullet.js')
argument_parser.add_argument(
    'action',
    help='Which action should we execute?',
    choices=['setup', 'build']
)
args = argument_parser.parse_args()

########## Setup ##########
def setup():

    print('========== Starting the setup ... ==========')

    ##### Emscripten #####
    emscripten_zip_file_name = EMSCRIPTEN_VERSION + '.zip'
    emscripten_url = 'https://github.com/kripken/emscripten/archive/' + emscripten_zip_file_name

    print('===== Starting to prepare ***emscripten*** ... =====')

    if os.path.isdir(EMSCRIPTEN_DIRECTORY):
        print('----- Emscripten already downloaded. -----')
    else:
        print('----- Starting to download emscripten v' + EMSCRIPTEN_VERSION + ' (' + emscripten_url + ') ... -----')
        emscripten_request = requests.get(emscripten_url)
        emscripten_zip_file = ZipFile(BytesIO(emscripten_request.content))
        emscripten_zip_file.extractall(THIRD_PARTY_DIR)

    print('===== ***Emscripten*** prepared. =====')

    ##### Bullet #####
    bullet_zip_file_name = BULLET_VERSION + '.zip'
    bullet_url = 'https://github.com/bulletphysics/bullet3/archive/' + bullet_zip_file_name

    print('===== Starting to prepare ***bullet*** ... =====')

    if os.path.isdir(BULLET_DIRECTORY):
        print('----- Bullet already downloaded. -----')
    else:
        print('----- Starting to download bullet v' + BULLET_VERSION + ' (' + bullet_url + ') ... -----')
        bullet_request = requests.get(bullet_url)
        bullet_zip_file = ZipFile(BytesIO(bullet_request.content))
        bullet_zip_file.extractall(THIRD_PARTY_DIR)

    print('===== ***Bullet*** prepared. =====')

    print('========== Setup completed! ==========')

    return True

########## Build ##########
def build():

    print('========== Starting the build ... ==========')

    # TODO: build the thing!

    print('========== Build completed! ==========')

    return True

########## Main ##########
if __name__ == '__main__':
    if args.action == 'setup':
        setup()
    elif args.action == 'build':
        build()
