#! /usr/bin/env python3

import sys, getopt, argparse, logging
from rockrover import core

import signal

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    sys.exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

def main():
    parser = argparse.ArgumentParser(description="RockRocker Control program.")
    parser.add_argument('-l', '--loglevel',
        action='store',
        dest="loglevel",
        default="info",
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        help="Setting the log level output")

    results = parser.parse_args()

    logging.basicConfig(stream=sys.stderr, level=results.loglevel.upper())
    logging.debug("DEBUG message")
    logging.info("INFO message")
    logging.warning("WARNING message")
    logging.error("ERROR message")
    logging.critical("CRITICAL message")

    _core = core.Core(
        inputDevices={
            'controller': '/dev/input/event0',
            'home': '/dev/input/event1',
        }
    )
    try:
        _core.go()
    finally:
        _core.close()

    sys.exit(0)
    
if __name__ == "__main__":
    main()
