# Bullet JS

A JS port of the C++ [Bullet3](https://github.com/bulletphysics/bullet3) physics engine.

**Note: It's still under heavy under development. I'm currently still learning emscripten & stuff.**


## Requirements

* `Python 3.5`
* [Emscripten](https://kripken.github.io/emscripten-site/docs/getting_started/downloads.html) -- it is also recommended to install [MinGW](https://kripken.github.io/emscripten-site/docs/building_from_source/toolchain_what_is_needed.html#compiler-toolchain) for windows


## Setup

* Run `pip3 install -r requirements.txt`
* Run `python3 bullet.py setup`


## Build

* Run `python3 bullet.py build`


## Development

Add your stuff into bullet.idl.


## FAQ

### Why not simply use [ammo.js](https://github.com/kripken/ammo.js)?

Valid question. That was also what I initially wanted (and did), but I ended up doing so much changes and refactoring, so decided to create a new project instead. Especially because there were a lot of changes between Ammo's version of Bullet (v2.82) and the once I wanted to port (v2.87).

## License(-s)
Bullet.js is licensed under the MIT license.
