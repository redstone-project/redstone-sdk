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

from RedstoneUtils.datatype.dicts import AttribDict


class TestDicts(unittest.TestCase):
    def test_attrib_dict(self):
        d = AttribDict()
        d.bar = 1
        d.val = "aaa"

        self.assertEqual(d.bar, 1)
        self.assertEqual(d.val, "aaa")
        self.assertEqual(d["bar"], 1)
        with self.assertRaises(AttributeError):
            v = d.not_exist
            v = d["not_exist"]
        self.assertEqual(d.get("not_exist"), None)


if __name__ == '__main__':
    unittest.main()
