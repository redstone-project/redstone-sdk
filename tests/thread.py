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
import time
import unittest

from silex.engines.thread import SingleThreadEngine, MultiThreadEngine


class TestThread(unittest.TestCase):
    def test_single_thread_engine(self):

        class SE(SingleThreadEngine):
            def _worker(self):
                while self.is_running():
                    self.ev.wait(1)
                    print("single working...")

        engine = SE(None, "TestSingleEngine")
        engine.start()

        self.assertTrue(engine.is_alive())
        self.assertTrue(engine.is_running())

        engine.stop()
        time.sleep(1)

        self.assertFalse(engine.is_alive())
        self.assertFalse(engine.is_running())

    def test_multi_thread_engine(self):
        class ME(MultiThreadEngine):
            def _worker(self):
                while self.is_running():
                    self.ev.wait(1)
                    print("multi working...")

        engine = ME(None, "TestMultiEngine", 4)
        engine.start()

        self.assertTrue(engine.is_alive())
        self.assertTrue(engine.is_running())

        engine.stop()
        time.sleep(1)

        self.assertFalse(engine.is_alive())
        self.assertFalse(engine.is_running())
