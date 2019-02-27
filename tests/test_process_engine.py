#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    class path
    ~~~~~~~~~~~~~~~~~~

    class desc

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2019 lightless. All rights reserved
"""
import time
import unittest

from silex.engines.process import SingleProcessEngine


class TestProcess(unittest.TestCase):

    def test_single_process_engine(self):

        class MyEngine(SingleProcessEngine):

            def _worker(self):
                print("my engine start!")

                cnt = 0

                # while status == EngineStatus.RUNNING:
                while self.is_running():
                    time.sleep(1)
                    cnt += 1
                    print("worker, cnt:", cnt)
                    print("current status:", self.status)

                print("my engine stop!")

        e = MyEngine("aaa", None)
        e.start()

        self.assertTrue(e.is_running())
        self.assertTrue(e.is_alive())

        print("let it run 5s...")
        time.sleep(5)

        print("now, stop it!")
        e.stop(wait=True)
        # e.process.join()

        print("kill done, check status!")
        print("is_running:", e.is_running())
        print("is_alive:", e.is_alive())
        self.assertFalse(e.is_running())
        self.assertFalse(e.is_alive())
