import os
import argparse
import configparser
from os.path import expanduser, join

import logging
logger = logging.getLogger(__name__)

INI_FILE = join(expanduser('~'), ".raspi-dashboard.ini")
LOCAL_DATA_DIR = join(expanduser('~'), ".raspi-dashboard")

CONFIG = config = configparser.ConfigParser()

config.read(INI_FILE)


def initialize_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spotify_client_id", type=str,
                        help="Your Spotify application Client Id")
    parser.add_argument("--spotify_client_secret", type=str,
                        help="Your Spotify application Client secret")

    args = parser.parse_args()

    if args.spotify_client_id is not None and args.spotify_client_secret is not None:
        _create_ini_file(args.spotify_client_id, args.spotify_client_secret)
    elif args.spotify_client_id is None and args.spotify_client_secret is None:
        pass
    else:
        logger.error(
            "Both [--spotify_client_id] and [--spotify_client_secret] are needed to initialize. Initialization failed.")
        parser.print_help()
        return

    if not os.path.exists(LOCAL_DATA_DIR):
        os.makedirs(LOCAL_DATA_DIR)


def _create_ini_file(spotify_client_id, spotify_client_secret):
    config['SPOTIFY'] = {
        'CLIENT_ID': spotify_client_id,
        'CLIENT_SECRET': spotify_client_secret,
    }

    with open(INI_FILE, 'w') as configfile:
        config.write(configfile)
