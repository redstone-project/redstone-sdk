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

        class SE(SingleProcessEngine):
            def _worker(self):
                cnt = 0
                print("app_ctx: {}".format(self.app_ctx))

                while self.is_running():
                    print("self.status: {}".format(self.status))
                    self.ev.wait(2)
                    cnt += 1
                    print("cnt:", cnt)
                    # self.ev.wait(100)

        app_ctx = {
            "a": 1,
            "foo": "bar",
        }

        e = SE(app_ctx, "TestSingleProcessEngine")
        e.start()

        self.assertTrue(e.is_running())
        self.assertTrue(e.is_alive())

        # self.assertIsInstance(e.pid(), int, "e.pid(): {}".format(e.pid()))
        print("e.pid(): {}".format(e.pid()))

        time.sleep(5)
        t1 = time.time()
        e.stop()
        time.sleep(1)
        print(time.time() - t1)
        # e.process.terminate()
        # time.sleep(5)

        self.assertFalse(e.is_alive())
        self.assertFalse(e.is_running())

# 方案一：直接使用terminate来结束进程
# 方案二：将shared variable传到每个进程中去，调用方无感知
