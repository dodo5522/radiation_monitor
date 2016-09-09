#!/usr/bin/env python
# -*- coding:utf-8 -*-

#   Copyright 2016 Takashi Ando - http://blog.rinka-blossom.com/
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import unittest
try:
    from unittest.mock import MagicMock, patch
except:
    from mock import MagicMock, patch
from radiation_monitor.source import GeigerMeter
import threading


class TestSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch("radiation_monitor.source.Serial", autospec=True)
    def test_(self, patched_serial):
        e_readline = threading.Event()
        e_callback = threading.Event()

        def mocked_readline():
            e_readline.wait()
            e_readline.clear()
            return b"20 [cpm]\n"

        def mocked_callback(val):
            e_callback.set()

        uart_port = MagicMock()
        uart_port.readline = MagicMock(side_effect=mocked_readline)
        patched_serial.return_value = uart_port
        callback = MagicMock(side_effect=mocked_callback)

        g = GeigerMeter("/dev/test", 15200, callback)

        g.start()

        self.assertTrue(g.is_alive())
        callback.assert_not_called()

        e_readline.set()

        self.assertTrue(g.is_alive())
        e_callback.wait(3)
        callback.assert_called_once_with(20 * 0.00812)

        g.stop()
        e_readline.set()
        g.join(60)

        self.assertFalse(g.is_alive())


if __name__ == "__main__":
    unittest.main()
