from . import app

import configparser
import argparse
import logging
import glob
import os

__loglevel = 'DEBUG'
__configfile = '/etc/rockrover/config.ini'


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog="RockRover",
        description="Mainprogram of RockRover"
    )
    parser.add_argument(
        '-l', '--loglevel',
        type=str.upper,
        help="Loglevel <DEBUG|INFO|WARNING|ERROR|CRITICAL|FATAL> [{__loglevel}]",
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'FATAL'],
        required=False
    )
    parser.add_argument(
        '-c', '--config',
        type=str,
        help="Path to config files [{__configfile}]",
        required=False
    )

    try:
        args = parser.parse_args()

        config = configparser.ConfigParser()
        config.read_dict({'DEFAULTS': {
            'loglevel': __loglevel},
            'LOGGING': {
                'loglevel': __loglevel
            }
        })

        if args.config is not None:
            if os.path.isfile(__configfile):
                config.read(glob.glob(args.config))

        if args.loglevel is not None:
            config.set(section='LOGGING', option='loglevel', value=args.loglevel)

        logging.basicConfig(level=config.get('LOGGING', 'loglevel'))

    except:
        logging.fatal('Could not even startup!')
        exit(1)

    rockrover = app.rockrover()
