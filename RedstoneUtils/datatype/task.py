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


class PriorityTask:
    def __init__(self, priority: int, data):
        self.data = data
        self.priority = int(priority)

    def __lt__(self, other: "PriorityTask"):
        return self.priority < other.priority

    def __str__(self):
        return "<PriorityTask || Priority: {} || data: {}>".format(self.priority, self.data)
