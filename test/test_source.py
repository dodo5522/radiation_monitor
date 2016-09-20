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
from collections import OrderedDict
from datetime import datetime
from radiation_monitor.source import GeigerMeter
from serial import SerialException
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

    @patch("radiation_monitor.source.datetime", autospec=True)
    @patch("radiation_monitor.source.Serial", autospec=True)
    def test_geiger_meter_sequence(self, patched_serial, pached_datetime):
        expected_cpm = 20

        unlock_readline = threading.Event()
        raise_serial_exception = threading.Event()

        def mocked_serial_close():
            unlock_readline.set()
            raise_serial_exception.set()

        def mocked_serial_readline():
            unlock_readline.wait()
            unlock_readline.clear()

            if raise_serial_exception.is_set():
                raise SerialException

            return "{} [cpm]\n".format(expected_cpm).encode("ascii")

        uart_port = MagicMock()
        uart_port.close = MagicMock(side_effect=mocked_serial_close)
        uart_port.readline = MagicMock(side_effect=mocked_serial_readline)
        patched_serial.return_value = uart_port
        pached_datetime.utcnow = MagicMock(return_value=datetime(2016, 1, 1))

        callback_called = threading.Event()

        def mocked_callback(name, data, now):
            callback_called.set()

        callback = MagicMock(side_effect=mocked_callback)

        g = GeigerMeter("hoge", "/dev/test", 15200, callback)
        g.start()

        self.assertTrue(g.is_alive())
        callback.assert_not_called()

        unlock_readline.set()

        self.assertTrue(g.is_alive())
        callback_called.wait()
        callback.assert_called_once_with(
            "hoge",
            OrderedDict({
                "Count Per Minute": OrderedDict({
                    "value": expected_cpm,
                    "unit": "cpm"
                }),
                "Micro Sievert Per Hour": OrderedDict({
                    "value": expected_cpm * 0.00812,
                    "unit": "usv"
                }),
            }),
            datetime(2016, 1, 1))

        g.stop()
        g.join()

        self.assertFalse(g.is_alive())


if __name__ == "__main__":
    unittest.main()
