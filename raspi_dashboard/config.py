import configparser
from os.path import expanduser, join

INI_FILE = join(expanduser('~'), ".raspi-dashboard.ini")
LOCAL_DATA_DIR = join(expanduser('~'), ".raspi-dashboard")

CONFIG = config = configparser.ConfigParser()

config.read(INI_FILE)
