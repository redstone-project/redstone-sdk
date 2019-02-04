#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    RedstoneUtils.engines.thread
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    基于thread的各种engine

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""


import multiprocessing
import threading
import typing

import abc

from ._base import CommonBaseEngine
from . import EngineStatus


class SingleThreadEngine(CommonBaseEngine):
    """
    基于单线程的引擎模块
    """

    def __init__(self, app_ctx, name=None):
        super(SingleThreadEngine, self).__init__()
        self.name = name if name else "SingleThreadEngine"
        self.app_ctx = app_ctx

    def start(self):
        self.status = EngineStatus.RUNNING
        self.thread: threading.Thread = threading.Thread(target=self._worker, name=self.name)
        self.thread.start()

    def stop(self, force=True):
        self.status = EngineStatus.STOP
        self.ev.set()

    def is_alive(self):
        return self.thread.is_alive()

    @abc.abstractmethod
    def _worker(self):
        pass


class MultiThreadEngine(CommonBaseEngine):
    """
    基于多线程的基础引擎
    """

    def __init__(self, app_ctx, name=None, pool_size=None):
        super(MultiThreadEngine, self).__init__()
        self.name = name if name else "MultiThreadEngine"
        self.app_ctx = app_ctx
        self.pool_size = pool_size if pool_size else multiprocessing.cpu_count() * 2 + 1

    def start(self):
        self.status = EngineStatus.RUNNING
        self.thread_pool: typing.List[threading.Thread] = \
            [threading.Thread(
                target=self._worker, name="{}-{}".format(self.name, idx)
            ) for idx in range(self.pool_size)]
        _ = [t.start() for t in self.thread_pool]

    def stop(self, force=True):
        if not force:
            while not self.app_ctx.MessageQueues.SEARCH_TASK_QUEUE.empty():
                self.ev.wait(1)
                continue
        self.status = EngineStatus.STOP
        self.ev.set()

    def is_alive(self):
        return any([t.is_alive() for t in self.thread_pool])

    @abc.abstractmethod
    def _worker(self):
        pass
