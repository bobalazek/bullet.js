#!/usr/bin/python

import os, sys, subprocess, argparse, pathlib
import requests
from io import BytesIO
from zipfile import ZipFile

########## Emscripten ##########
exec(open(os.path.expanduser('~/.emscripten'), 'r').read())

try:
    EMSCRIPTEN_ROOT
except:
    print('EMSCRIPTEN not found. Please install it first.')
    sys.exit(1)

sys.path.append(EMSCRIPTEN_ROOT)
import tools.shared as emscripten

########## Configuration ##########
##### General #####
ROOT = os.path.dirname(os.path.realpath(__file__))
THIRD_PARTY_DIR = os.path.join(ROOT, 'third_party')
BUILD_FILE_NAME = 'bullet.js'

##### Bullet #####
BULLET_VERSION = '2.87'
BULLET_DIRECTORY = os.path.join(THIRD_PARTY_DIR, 'bullet3-' + BULLET_VERSION)
BULLET_ZIP_FILE_NAME = BULLET_VERSION + '.zip'
BULLET_ZIP_URL = 'https://github.com/bulletphysics/bullet3/archive/' + BULLET_ZIP_FILE_NAME
BULLET_INCLUDES = []

# Populate the bullet includes
BULLET_INCLUDES = [
    os.path.join(BULLET_DIRECTORY, 'src', 'LinearMath', 'btVector3.h'),
    os.path.join(BULLET_DIRECTORY, 'src', 'LinearMath', 'btQuadWord.h'),
    os.path.join(BULLET_DIRECTORY, 'src', 'LinearMath', 'btQuaternion.h'),
]

# TODO
# BULLET_SRC_DIRECTORY = os.path.join(BULLET_DIRECTORY, 'src')
# for root, dirs, files in os.walk(BULLET_SRC_DIRECTORY):
#     for name in files:
#         if name.endswith((".h")):
#             BULLET_INCLUDES.append(os.path.join(root, name))

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

    ##### Bindings #####
    emscripten_binder_args = [
        emscripten.PYTHON,
        os.path.join(EMSCRIPTEN_ROOT, 'tools', 'webidl_binder.py'),
        os.path.join(ROOT, 'bullet.idl'),
        'glue'
    ]

    ### Generate
    print('=== Generating emscripten bindings ... ===')
    print('----- Binder args: ' + ' '.join(emscripten_binder_args) + ' -----')

    subprocess.Popen(emscripten_binder_args).communicate()

    ### Build
    emscripten_args = [
        '-O3',
        '--llvm-lto', '1',
        '-s', 'NO_EXIT_RUNTIME=1',
        '-s', 'NO_FILESYSTEM=1',
        '-s', 'EXPORTED_RUNTIME_METHODS=[]',
        '-s', 'AGGRESSIVE_VARIABLE_ELIMINATION=1',
        '-s', 'ELIMINATE_DUPLICATE_FUNCTIONS=1',
        '-s', 'SINGLE_FILE=1',
        '-s', 'NO_DYNAMIC_EXECUTION=1',
        '-s', 'EXPORT_NAME="Bullet"',
        '-s', 'MODULARIZE=1',
    ]

    for include in BULLET_INCLUDES:
        # include = include.replace(ROOT, '').lstrip(' \\/\t\n\r')
        emscripten_args += ['-include', include]

    print('=== Building emscripten bindings ... ===')
    print('Binder args: ' + ' '.join(emscripten_args))

    emscripten.Building.emcc('glue.cpp', emscripten_args,
                             os.path.join(ROOT, 'build', BUILD_FILE_NAME))

    print('========== Build completed! ==========')

    return True

########## Main ##########
if __name__ == '__main__':
    if args.action == 'setup':
        setup()
    elif args.action == 'build':
        build()
