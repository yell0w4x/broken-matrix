# Broken matrix

<p align="center">
    <img src="https://github.com/yell0w4x/assets/blob/52a498a21798f2fb3d542c71ad0b32748d6c3034/bmatrix.gif" alt="bmatrix"/>
</p>

```
pip install broken-matrix
```

Then

```
$ bmatrix --help
usage: bmatrix [-h] [--objects-limit OBJECTS_LIMIT] [--random-trace-color]

Broken matrix. Objects can collide and bounce off each other.

Keys available in runtime:

    'i' - show info
    'r' - use random color for objects trace
    '+' - increase objects limit 
    '-' - decrease objects limit 
    'q' - exit

options:
  -h, --help            show this help message and exit
  --objects-limit OBJECTS_LIMIT
                        Below this number objects bounce off the edges. If this number exceeded objects are allowed to go off the screen
  --random-trace-color  Use random objects trace color
```