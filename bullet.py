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
BULLET_ZIP_FILE_NAME = BULLET_VERSION + '.zip'
BULLET_ZIP_URL = 'https://github.com/bulletphysics/bullet3/archive/' + BULLET_ZIP_FILE_NAME

##### Emscripten #####
EMSCRIPTEN_VERSION = '1.37.33'
EMSCRIPTEN_DIRECTORY = os.path.join(THIRD_PARTY_DIR, 'emscripten-' + EMSCRIPTEN_VERSION)
EMSCRIPTEN_ZIP_FILE_NAME = EMSCRIPTEN_VERSION + '.zip'
EMSCRIPTEN_ZIP_URL = 'https://github.com/kripken/emscripten/archive/' + EMSCRIPTEN_ZIP_FILE_NAME

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
    print('===== Starting to prepare EMSCRIPTEN ... =====')

    if os.path.isdir(EMSCRIPTEN_DIRECTORY):
        print('----- EMSCRIPTEN already downloaded. -----')
    else:
        print('----- Starting to download EMSCRIPTEN v' + EMSCRIPTEN_VERSION + ' (' + EMSCRIPTEN_ZIP_URL + ') ... -----')
        emscripten_request = requests.get(EMSCRIPTEN_ZIP_URL)
        emscripten_zip_file = ZipFile(BytesIO(emscripten_request.content))
        emscripten_zip_file.extractall(THIRD_PARTY_DIR)

    print('===== EMSCRIPTEN prepared. =====')

    ##### Bullet #####
    print('===== Starting to prepare BULLET ... =====')

    if os.path.isdir(BULLET_DIRECTORY):
        print('----- BULLET already downloaded. -----')
    else:
        print('----- Starting to download BULLET v' + BULLET_VERSION + ' (' + BULLET_ZIP_URL + ') ... -----')
        bullet_request = requests.get(BULLET_ZIP_URL)
        bullet_zip_file = ZipFile(BytesIO(bullet_request.content))
        bullet_zip_file.extractall(THIRD_PARTY_DIR)

    print('===== BULLET prepared. =====')

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
