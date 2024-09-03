from .roles import env_setup, zookeeper, kafka
from .helpers.main import *


def start():
	check_flags()
	check_creds_yml()
	introduce()
	while True:
		break

