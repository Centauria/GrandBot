# -*- coding: utf-8 -*-
import atexit
from pymongo import MongoClient

from util import configuration

client = MongoClient(
    configuration.mongodb.host,
    username=configuration.mongodb.user,
    password=configuration.mongodb.pwd,
    authSource='admin',
    authMechanism='SCRAM-SHA-256'
)
db = client[configuration.mongodb.db]


@atexit.register
def on_exit():
    print('MongoDB Connection closing...')
    client.close()
