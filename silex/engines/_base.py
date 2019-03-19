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


import abc

from .constant import engine_status


class CommonBaseEngine(object):

    def __init__(self):
        super(CommonBaseEngine, self).__init__()

        # 引擎的名称
        self.name = "BaseEngine"

        # 引擎的状态，实例化后默认为 READY 状态
        self.status = engine_status.READY

    def is_running(self):
        return self.status == engine_status.RUNNING

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass

    @abc.abstractmethod
    def is_alive(self):
        pass
