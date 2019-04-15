#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    silex.queue.rabbit
    ~~~~~~~~~~~~~~~~~~

    RabbitMQ队列的封装

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2019 lightless. All rights reserved
"""

import typing

import pika
from pika.adapters.blocking_connection import BlockingChannel


class RabbitQueue(object):
    def __init__(self):
        super(RabbitQueue, self).__init__()

        self.rabbit_connection: typing.Optional[pika.BlockingConnection] = None

    def connect(self, username, password, host, vhost="/"):
        cred = pika.PlainCredentials(username, password)
        self.rabbit_connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host, virtual_host=vhost, credentials=cred
            )
        )

    def get_new_channel(self) -> BlockingChannel:
        return self.rabbit_connection.channel()
