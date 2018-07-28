#!/usr/bin/env python3

import sys
sys.path.append('@PYTHONDIR@')

from package_breeder import main

if __name__ == '__main__':

    package_breeder_main = main.Main(sys.argv[0], '@PACKAGE_STRING@')

    if (len(sys.argv) < 3):
        package_breeder_main.print_usage()
        sys.exit(-1)

    base_dir = sys.argv[1]
    command = sys.argv[2]
    arguments = sys.argv[3:]

    try:
        package_breeder_main.run(base_dir, command, arguments)
    except (OSError, ValueError) as e:
        print('ERROR: Interrupted while hatching (%s)! Aborting.' % str(e))
        sys.exit(-1)

    sys.exit(0)
