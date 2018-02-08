# Bullet JS

A JS port of the C++ [Bullet3](https://github.com/bulletphysics/bullet3) physics engine.

**Note: It's still under heavy under development. I'm currently still learning emscripten & stuff.**


## Requirements

* `Python 3.5`


## Setup

* Run `python bullet.py setup`


## Build

* Run `python bullet.py build`


## Development

Add your stuff into bullet.idl.


## FAQ

### Why not simply use [ammo.js](https://github.com/kripken/ammo.js)?

Valid question. That was also what I initially wanted (and did), but I ended up doing so much changes and refactoring, so decided to create a new project instead. Especially because there were a lot of changes between Ammo's version of Bullet (v2.82) and the once I wanted to port (v2.87).
