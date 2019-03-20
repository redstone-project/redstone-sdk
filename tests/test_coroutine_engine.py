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

from silex.engines.coroutine import CoroutinePoolEngine


class TestCoroutineEngine(unittest.TestCase):

    def test_coroutine_pool(self):
        class MyEngine(CoroutinePoolEngine):

            async def _worker(self, idx):
                self._init_event()
                current_name = "{}-{}".format(self.name, idx)
                print("{} My engine start!".format(current_name))
                cnt = 0
                while self.is_running():
                    await self._wait(1)
                    # await asyncio.sleep(1)
                    # await self.ev.wait()
                    cnt += 1
                    print("{}, current cnt: {}".format(current_name, cnt))
                print("{} My engine stop!".format(current_name))

        e = MyEngine("TestCoroutine", pool_size=2)
        e.start()

        self.assertTrue(e.is_running())
        self.assertTrue(e.is_alive())

        print("let it run 5s...")
        time.sleep(5)

        print("now stop it!")
        e.stop(wait=True)

        print("kill done, check status!")
        self.assertFalse(e.is_running())
        self.assertFalse(e.is_alive())
