from bmatrix.stage import TerminalStage
from bmatrix.particle import Particle, trace_color

from blessed import Terminal
import time
import random
from datetime import datetime, timedelta
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter


def cli(args=sys.argv[1:]):
    desc = """
Broken matrix. Objects can collide and bounce off each other.

Keys available in runtime:\n
    'i' - show info
    'r' - use random color for objects trace
    '+' - increase objects limit 
    '-' - decrease objects limit 
    'q' - exit"""

    parser = ArgumentParser(description=desc, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('--objects-limit', default=150, type=int, required=False, 
        help='Below this number objects bounce off the edges. If this number exceeded objects are allowed to go off the screen')
    parser.add_argument('--random-trace-color', default=False, required=False, action='store_true',
        help='Use random objects trace color')

    return parser.parse_args(args)


def main():
    args = cli()
    term = Terminal()
    stage = TerminalStage(term, args.objects_limit)

    show_info = False
    stage.clear()
    while True:
        stage.run()

        with term.cbreak():
            val = term.inkey(timeout=0)
            match val.lower():
                case 'i':
                    show_info = not show_info
                    if not show_info:
                        stage.clear()

                case 'r':
                    args.random_trace_color = not args.random_trace_color

                case '+':
                    stage.objects_limit(stage.objects_limit() + 1)

                case '-':
                    limit = stage.objects_limit() - 1
                    if limit < 0:
                        limit = 0
                    stage.objects_limit(limit)

                case 'q':   
                    break

        for _ in range(2):
            stage.add_particle(Particle(random.randrange(0, stage.width() - 1), 0, 
                                        0, 0.5 + random.random() * 0.5, 
                                        trace_limit=stage.height() // 1.5, 
                                        trace_color=trace_color(args.random_trace_color), 
                                        head_color=(0xcc, 0xff, 0xcc)))

        if show_info:
            def print_line(label, value):
                print(f'{term.yellow3}{label:>15}{value:>4}{term.normal}')

            with term.location(0, 0):
                print_line('Objects:', len(stage.objects()))
                print_line('Objects limit:', stage.objects_limit())
                print_line('Stage width:', stage.width())
                print_line('Stage height:', stage.height())
        
        time.sleep(0.025)


if __name__ == '__main__':
    main()