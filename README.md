# Broken matrix

<p align="center">
    <img src="https://github.com/yell0w4x/assets/blob/e128cb0a292a7b571d1d9d73da80b76d00a83037/bmatrix.gif" alt="bmatrix"/>
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