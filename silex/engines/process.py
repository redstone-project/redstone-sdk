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
import multiprocessing

from silex.engines import EngineStatus
from silex.engines._base import CommonBaseEngine


class SingleProcessEngine(CommonBaseEngine):
    """
    基于单进程的引擎模块
    """

    def __init__(self, app_ctx, name=None):
        super(SingleProcessEngine, self).__init__()

        # 引擎的名称
        self.name = name if name else "SingleProcessEngine"

        # 外层的APP context，如果没有则留None
        self.app_ctx = app_ctx

        # 引擎的主进程
        self.process: multiprocessing.Process = None

        # 引擎的event对象
        self.ev: multiprocessing.Event = None

    def start(self):
        self.ev: multiprocessing.Event = multiprocessing.Event()
        self.status = EngineStatus.RUNNING
        self.process = multiprocessing.Process(target=self._worker, name=self.name)
        self.process.start()

    def stop(self):
        self.status = EngineStatus.STOP
        # self.ev.set()
        self.process.terminate()

    def is_alive(self):
        return self.process.is_alive()

    def pid(self):
        return self.process.pid

    @abc.abstractmethod
    def _worker(self):
        pass
