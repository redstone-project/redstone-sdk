#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    silex.engines.coroutine
    ~~~~~~~~~~~~~~~~~~~~~~~

    基于coroutine的引擎类

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import abc
import asyncio
import multiprocessing
import threading

from silex.engines.constant import engine_status
from silex.engines._base import CommonBaseEngine


class CoroutineEngine(CommonBaseEngine):
    """
    基于单协程的引擎模块
    """
    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def is_alive(self):
        raise NotImplementedError


class CoroutinePoolEngine(CommonBaseEngine):
    """
    基于协程池的引擎模块
    """

    def __init__(self, app_ctx, name=None, pool_size=None):
        super(CoroutinePoolEngine, self).__init__()

        # name
        self.name = name if name else "MultiCoroutineEngine"

        # outer app_ctx
        self.app_ctx = app_ctx

        # coroutine pool size
        self.pool_size = pool_size if pool_size else multiprocessing.cpu_count() * 2 + 1

        # hold coroutine's thread
        self.coroutine_thread: threading.Thread = None

        # event object
        self.ev: asyncio.Event = None

        # loop object
        self.main_loop = None

    def start(self):
        """开启一个新的线程来容纳协程池"""
        self.status = engine_status.RUNNING
        self.ev = asyncio.Event()
        self.coroutine_thread = threading.Thread(target=self._loader, name=self.name)
        self.coroutine_thread.start()

    def stop(self, wait=False, timeout=None):
        self.status = engine_status.STOP
        self.ev.set()
        if wait:
            self.coroutine_thread.join(timeout)

    def is_alive(self):
        """线程的状态就是协程池的状态"""
        return self.coroutine_thread.is_alive()

    def _loader(self):
        """启动协程池"""

        # 创建新的event_loop
        self.main_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.main_loop)

        # 加载工作协程
        target = [
            self._worker(idx) for idx in range(self.pool_size)
        ]
        self.main_loop.run_until_complete(asyncio.gather(*target))

    @abc.abstractmethod
    async def _worker(self, idx):
        pass
