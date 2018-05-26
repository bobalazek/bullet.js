#!/usr/bin/python

import os, sys, shutil, subprocess, argparse, pathlib, multiprocessing
import requests
from io import BytesIO
from zipfile import ZipFile
from data.data import get_bullet_includes, get_bullet_archive_includes, get_idl_file_paths

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

########## Arguments ##########
argument_parser = argparse.ArgumentParser(description='Bullet.js')
argument_parser.add_argument(
    'action',
    help='Which action should we execute?',
    choices=['setup', 'build']
)
argument_parser.add_argument(
    '--wasm',
    help="Should it be an wasm build?",
    action="store_true"
)
argument_parser.add_argument(
    '--rebuild-bullet',
    help="Should the bullet lib be rebuild?",
    action="store_true"
)
args = argument_parser.parse_args()

########## Configuration ##########
##### General #####
ROOT = os.path.dirname(os.path.realpath(__file__))
IS_WASM_BUILD = args.wasm
THIRD_PARTY_DIR = os.path.join(ROOT, 'third_party')
BUILD_FILE_NAME = 'bullet.wasm.js' if IS_WASM_BUILD else 'bullet.js'
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
BULLET_MAKE_DIRECTORY = os.path.join(BULLET_DIRECTORY, 'make_build')
BULLET_ARCHIVE_INCLUDES = get_bullet_archive_includes(BULLET_MAKE_DIRECTORY)
BULLET_FORCE_BUILD = args.rebuild_bullet # should we force the bullet to be build?

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
    if not os.path.exists(BULLET_MAKE_DIRECTORY) or BULLET_FORCE_BUILD:
        print('===== Building BULLET ... =====')

        if BULLET_FORCE_BUILD and os.path.exists(BULLET_MAKE_DIRECTORY):
            shutil.rmtree(BULLET_MAKE_DIRECTORY)

        if not os.path.exists(BULLET_MAKE_DIRECTORY):
            os.makedirs(BULLET_MAKE_DIRECTORY)

        os.chdir(BULLET_MAKE_DIRECTORY)

        # CMake
        bullet_cmake_args = [
            emscripten.PYTHON,
            os.path.join(EMSCRIPTEN_ROOT, 'emcmake'),
            'cmake',
            '..',
            '-DBUILD_DEMOS=OFF',
            '-DBUILD_EXTRAS=OFF',
            '-DBUILD_CPU_DEMOS=OFF',
            '-DUSE_GLUT=OFF',
            '-DBUILD_PYBULLET=OFF',
            '-DCMAKE_BUILD_TYPE=Release',
        ]
        emscripten.Building.configure(bullet_cmake_args)

        CORES = multiprocessing.cpu_count()

        # Make
        bullet_make_args = [
            emscripten.PYTHON,
            os.path.join(EMSCRIPTEN_ROOT, 'emmake'),
            'make',
            '-j' + str(CORES),
        ]
        emscripten.Building.make(bullet_make_args)

        os.chdir(ROOT)

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

    ### Generate
    print('===== Generating emscripten bindings ... =====')

    emscripten_binder_args = [
        emscripten.PYTHON,
        os.path.join(EMSCRIPTEN_ROOT, 'tools', 'webidl_binder.py'),
        IDL_FILE_PATH,
        'glue'
    ]
    subprocess.Popen(emscripten_binder_args).communicate()

    ### Build
    emscripten_args = [
        '-O3',
        '--llvm-lto', '1',
        '-s', 'NO_EXIT_RUNTIME=1',
        '-s', 'NO_FILESYSTEM=1',
        '-s', 'EXPORTED_RUNTIME_METHODS=[]',
        '-s', 'LEGACY_VM_SUPPORT=1',
        '-s', 'NO_DYNAMIC_EXECUTION=1',
    ]
    if IS_WASM_BUILD:
        emscripten_args = emscripten_args + [
            '-s', 'WASM=1',
            '-s', 'BINARYEN_IGNORE_IMPLICIT_TRAPS=1',
            '-s', 'BINARYEN_TRAP_MODE="allow"',
        ]
    else:
        emscripten_args = emscripten_args + [
            '-s', 'AGGRESSIVE_VARIABLE_ELIMINATION=1',
            '-s', 'ELIMINATE_DUPLICATE_FUNCTIONS=1',
            '-s', 'SINGLE_FILE=1',
        ]

    emscripten_final_args = emscripten_args + [
        '-s', 'EXPORT_NAME="Bullet"',
        '-s', 'MODULARIZE=1',
        '-s', 'TOTAL_MEMORY=%d' % (512 * 1024 * 1024),
    ]

    print('===== Building emscripten bindings ... =====')

    emscripten_args = emscripten_args + [
        '-I', BULLET_SRC_DIRECTORY_RELATIVE,
        '-c',
    ]
    for include in BULLET_INCLUDES:
        include = include.replace(ROOT, '').lstrip(' \\/\t\n\r')
        emscripten_args += ['-include', include]

    emscripten.Building.emcc(
        'glue.cpp',
        emscripten_args,
        'glue.bc'
    )

    emscripten.Building.link(
        ['glue.bc'] + BULLET_ARCHIVE_INCLUDES,
        'libglue.bc'
    )

    emscripten.Building.emcc(
        'libglue.bc',
        emscripten_final_args,
        BUILD_FILE_PATH
    )

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
