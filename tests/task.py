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
import unittest
from queue import PriorityQueue

from RedstoneUtils.datatype.task import PriorityTask


class TestPriorityTask(unittest.TestCase):

    def test_task(self):
        q = PriorityQueue(maxsize=8)

        task1 = PriorityTask(100, "task-1")
        task2 = PriorityTask(6, "task-2")

        q.put(task1)
        q.put(task2)

        self.assertEqual(q.get(), task2)
        self.assertEqual(q.get(), task1)


if __name__ == '__main__':
    unittest.main()
