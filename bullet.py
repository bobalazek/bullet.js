#!/usr/bin/python

import os, sys, subprocess, argparse, pathlib, multiprocessing
import requests
from io import BytesIO
from zipfile import ZipFile
from data.data import get_bullet_includes, get_idl_file_paths

########## Emscripten ##########
EMSCRIPTEN_USER_FILE = os.path.expanduser('~/.emscripten')
if not os.path.isfile(EMSCRIPTEN_USER_FILE):
    print('EMSCRIPTEN not found. Please install it first.')
    sys.exit(1)

exec(open(EMSCRIPTEN_USER_FILE, 'r').read())

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
BUILD_FILE_PATH = os.path.join(ROOT, 'build', BUILD_FILE_NAME)
IDL_FILE_PATH = os.path.join(ROOT, 'bindings.idl')
IDL_FILE_PATHS = get_idl_file_paths(ROOT)

##### Bullet #####
BULLET_VERSION = 'master' # '2.87' # issue because: https://github.com/bulletphysics/bullet3/pull/1409
BULLET_DIRECTORY = os.path.join(THIRD_PARTY_DIR, 'bullet3-' + BULLET_VERSION)
BULLET_ZIP_FILE_NAME = BULLET_VERSION + '.zip'
BULLET_ZIP_URL = 'https://github.com/bulletphysics/bullet3/archive/' + BULLET_ZIP_FILE_NAME
BULLET_INCLUDES = get_bullet_includes(BULLET_DIRECTORY)
BULLET_SRC_DIRECTORY_RELATIVE = os.path.join('third_party', 'bullet3-' + BULLET_VERSION, 'src')
BULLET_FORCE_BUILD = False # should we force the bullet to be build?

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
    if not os.path.isdir(BULLET_DIRECTORY):
        print('BULLET not found. Please run "python bullet.py setup" first.')
        sys.exit(1)

    print('========== Starting the build ... ==========')

    ### Build Bullet
    bullet_cmake_cache_file_path = os.path.join(BULLET_DIRECTORY, 'CMakeCache.txt')
    if not os.path.isfile(bullet_cmake_cache_file_path) or BULLET_FORCE_BUILD:
        print('===== Building BULLET ... =====')

        if os.path.isfile(bullet_cmake_cache_file_path):
            os.remove(bullet_cmake_cache_file_path)

        bullet_cmake_args = [
            emscripten.PYTHON,
            os.path.join(EMSCRIPTEN_ROOT, 'emcmake'),
            'cmake',
            '.',
            '-DBUILD_DEMOS=OFF',
            '-DBUILD_EXTRAS=OFF',
            '-DBUILD_CPU_DEMOS=OFF',
            '-DUSE_GLUT=OFF',
            '-DBUILD_PYBULLET=OFF',
            '-DCMAKE_BUILD_TYPE=Release',
        ]
        subprocess.Popen(bullet_cmake_args, cwd=BULLET_DIRECTORY).communicate()

        CORES = multiprocessing.cpu_count()
        bullet_make_args = [
            emscripten.PYTHON,
            os.path.join(EMSCRIPTEN_ROOT, 'emmake'),
            'make',
            '-j' + CORES,
        ]
        subprocess.Popen(bullet_make_args, cwd=BULLET_DIRECTORY).communicate()

    ### Concat IDLs
    idl_file_content = ''
    for include in IDL_FILE_PATHS:
        idl_file_content += '////////// ' + \
            include.replace(ROOT, '').lstrip(' \\/\t\n\r') + \
            ' //////////'
        idl_file_content += '\n\n'
        idl_file_content += open(include).read()
        idl_file_content += '\n\n\n\n'

    open(IDL_FILE_PATH, 'w').write(idl_file_content)

    emscripten_binder_args = [
        emscripten.PYTHON,
        os.path.join(EMSCRIPTEN_ROOT, 'tools', 'webidl_binder.py'),
        IDL_FILE_PATH,
        'glue'
    ]

    ### Generate
    print('===== Generating emscripten bindings ... =====')
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
        '-I', BULLET_SRC_DIRECTORY_RELATIVE,
    ]

    for include in BULLET_INCLUDES:
        include = include.replace(ROOT, '').lstrip(' \\/\t\n\r')
        emscripten_args += ['-include', include]

    print('===== Building emscripten bindings ... =====')
    print('----- Binder args: ' + ' '.join(emscripten_args) + ' -----')

    emscripten.Building.emcc(
        'glue.cpp', emscripten_args, BUILD_FILE_PATH)

    build_content = '// Bullet.js is a port of C++ Bullet3 Physics (zlib licensed).\n'
    build_content += open(BUILD_FILE_PATH).read()
    open(BUILD_FILE_PATH, 'w').write(build_content)

    print('========== Build completed! ==========')

    return True

########## Main ##########
if __name__ == '__main__':
    if args.action == 'setup':
        setup()
    elif args.action == 'build':
        build()
