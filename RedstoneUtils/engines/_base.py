#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    class path
    ~~~~~~~~~~~~~~~
    Class description.

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import threading
from typing import List
import abc

from . import EngineStatus


class CommonBaseEngine(object):

    def __init__(self):
        super(CommonBaseEngine, self).__init__()
        self.name = "BaseEngine"
        self.status = EngineStatus.READY
        self.ev: threading.Event = threading.Event()
        self.thread: threading.Thread = None
        self.thread_pool: List[threading.Thread] = None

    def is_running(self):
        return self.status == EngineStatus.RUNNING

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self, force=True):
        pass

    @abc.abstractmethod
    def is_alive(self):
        pass

    @abc.abstractmethod
    def _worker(self):
        pass
