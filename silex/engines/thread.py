#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    silex.engines.thread
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    基于thread的各种engine

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2019 lightless. All rights reserved
"""


import multiprocessing
import threading
import typing

import abc

from ._base import CommonBaseEngine
from .constant import engine_status


class ThreadEngine(CommonBaseEngine):
    """
    基于单线程的引擎模块
    """

    def __init__(self, app_ctx, name=None):
        super(ThreadEngine, self).__init__()

        # 引擎的名称
        self.name = name if name else "SingleThreadEngine"

        # 外层的app context，如果没有可以留None
        self.app_ctx = app_ctx

        # 引擎的主线程
        self.thread: threading.Thread = None

        # 引擎的event对象
        self.ev: threading.Event = None

    def start(self):
        self.status = engine_status.RUNNING
        self.thread: threading.Thread = threading.Thread(target=self._worker, name=self.name)
        self.thread.start()

    def stop(self):
        self.status = engine_status.STOP
        self.ev.set()

    def is_alive(self):
        return self.thread.is_alive()

    @abc.abstractmethod
    def _worker(self):
        pass


class ThreadPoolEngine(CommonBaseEngine):
    """
    基于多线程的基础引擎
    """

    def __init__(self, app_ctx, name=None, pool_size=None):
        super(ThreadPoolEngine, self).__init__()

        # 引擎的名称
        self.name = name if name else "MultiThreadEngine"

        # 外层的app context，如果无用则留None
        self.app_ctx = app_ctx

        # 线程池的大小，默认为 2 * count(cpu) + 1
        self.pool_size = pool_size if pool_size else multiprocessing.cpu_count() * 2 + 1

        # 引擎的主线程池
        self.thread_pool: typing.List[threading.Thread] = None

        # 引擎的event对象
        self.ev: threading.Event = None

    def start(self):
        self.status = engine_status.RUNNING
        self.thread_pool: typing.List[threading.Thread] = \
            [threading.Thread(
                target=self._worker, name="{}-{}".format(self.name, idx)
            ) for idx in range(self.pool_size)]
        map(lambda t: t.start(), self.thread_pool)

    def stop(self):
        self.status = engine_status.STOP
        self.ev.set()

    def is_alive(self):
        return any([t.is_alive() for t in self.thread_pool])

    @abc.abstractmethod
    def _worker(self):
        pass
