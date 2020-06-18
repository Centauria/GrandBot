# -*- coding: utf-8 -*-
from iotbot import GroupMsg
import util.db.mongodb.operation as op


def receive_events(ctx: dict):
    print(f'{ctx}')
