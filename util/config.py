# -*- coding: utf-8 -*-
from pyhocon import ConfigFactory


def load_config():
    config = ConfigFactory.parse_file('../config.conf')
    return config
