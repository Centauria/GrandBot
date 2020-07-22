# -*- coding: utf-8 -*-
from pyhocon import ConfigFactory

configuration = ConfigFactory.parse_file('config.conf')


def reload_config():
	return ConfigFactory.parse_file('config.conf')
