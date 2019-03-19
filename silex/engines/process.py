#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    silex.engines.process
    ~~~~~~~~~~~~~~~~~~~~~

    基于process的引擎类

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2019 lightless. All rights reserved
"""
import abc
import ctypes
import multiprocessing
from typing import List

from silex.engines.constant import engine_status
from silex.engines._base import CommonBaseEngine


class ProcessEngine(CommonBaseEngine):
    """
    基于单进程的引擎模块
    """

    def __init__(self, name, app_ctx=None):
        super(ProcessEngine, self).__init__()
        self._manager = multiprocessing.Manager()

        # 引擎的名称
        self.name = name if name else "SingleProcessEngine"

        # 外层的APP context，如果没有则留None
        self.app_ctx = app_ctx

        # 引擎的主进程
        self.process: multiprocessing.Process = None

        # 引擎的event对象
        self.ev: multiprocessing.Event = None

        # 引擎的status
        self.status: ctypes.c_int = self._manager.Value("i", engine_status.READY)

    def start(self):
        self.ev: multiprocessing.Event = self._manager.Event()
        self.status.value = engine_status.RUNNING
        self.process = multiprocessing.Process(target=self._worker, name=self.name)
        self.process.start()

    def stop(self, wait=False, timeout=None):
        self.status.value = engine_status.STOP
        self.ev.set()
        if wait:
            self.process.join(timeout)

    def is_alive(self):
        return self.process.is_alive()

    def pid(self):
        return self.process.pid

    def is_running(self):
        return self.status.value == engine_status.RUNNING

    @abc.abstractmethod
    def _worker(self):
        pass


class ProcessPoolEngine(CommonBaseEngine):
    """
    基于进程池的引擎
    """

    def __init__(self, name, app_ctx=None, pool_size=None):
        super(ProcessPoolEngine, self).__init__()
        self._manager = multiprocessing.Manager()

        self.name = name if name else "DefaultProcessPool"
        self.app_ctx = app_ctx

        self.status: ctypes.c_int = self._manager.Value("i", engine_status.READY)
        self.ev = self._manager.Event()

        self.pool_size = pool_size if pool_size else multiprocessing.cpu_count()
        self.pool: List[multiprocessing.Process] = []

    def start(self):
        self.status.value = engine_status.RUNNING
        self.pool = [multiprocessing.Process(
            target=self._worker, name="{}-{}".format(self.name, idx)
        ) for idx in range(self.pool_size)]
        [p.start() for p in self.pool]

    def stop(self, wait=False, timeout=None):
        self.status.value = engine_status.STOP
        self.ev.set()
        if wait:
            [p.join(timeout) for p in self.pool]

    def is_running(self):
        return self.status.value == engine_status.RUNNING

    def is_alive(self):
        return any([p.is_alive() for p in self.pool])

    @abc.abstractmethod
    def _worker(self):
        pass
