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

    parser.add_argument("--inky_colour", type=str,
                        choices=["red", "black", "yellow"], help="Your Inky colour")

    parser.add_argument("--spotify_client_id", type=str,
                        help="Your Spotify application Client Id")
    parser.add_argument("--spotify_client_secret", type=str,
                        help="Your Spotify application Client secret")
    parser.add_argument("--spotify_redirect_uri", type=str,
                        help="Your Spotify application redirect URI")

    args = parser.parse_args()

    inky_colour = args.inky_colour if args.inky_colour is not None else config['INKY'].get(
        'colour', "") if config.has_section('INKY') else ""

    spotify_client_id = args.spotify_client_id if args.spotify_client_id is not None else config['SPOTIFY'].get(
        'client_id', "") if config.has_section('SPOTIFY') else ""
    spotify_client_secret = args.spotify_client_secret if args.spotify_client_secret is not None else config['SPOTIFY'].get(
        'client_secret', "") if config.has_section('SPOTIFY') else ""
    spotify_redirect_uri = args.spotify_redirect_uri if args.spotify_redirect_uri is not None else config['SPOTIFY'].get(
        'redirect_uri', "") if config.has_section('SPOTIFY') else ""

    _create_ini_file(inky_colour, spotify_client_id,
                     spotify_client_secret, spotify_redirect_uri)

    if not os.path.exists(LOCAL_DATA_DIR):
        os.makedirs(LOCAL_DATA_DIR)


def _create_ini_file(inky_colour, spotify_client_id, spotify_client_secret, spotify_redirect_uri):
    config['INKY'] = {
        'colour': inky_colour
    }

    config['SPOTIFY'] = {
        'client_id': spotify_client_id,
        'client_secret': spotify_client_secret,
        'redirect_uri': spotify_redirect_uri,
    }

    with open(INI_FILE, 'w') as configfile:
        config.write(configfile)
