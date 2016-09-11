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
from radiation_monitor import argparser


class TestArgParser(unittest.TestCase):
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

    def test_default_args(self):
        parsed = argparser.init(["/dev/tty.usbserial", "19200"])

        self.assertEqual("/dev/tty.usbserial", parsed.serial_device_path[0])
        self.assertEqual(19200, parsed.serial_baudrate[0])
        self.assertEqual(None, parsed.xively_api_key)
        self.assertEqual(None, parsed.xively_feed_key)
        self.assertEqual(None, parsed.keenio_project_id)
        self.assertEqual(None, parsed.keenio_write_key)
        self.assertEqual(None, parsed.twitter_consumer_key)
        self.assertEqual(None, parsed.twitter_consumer_secret)
        self.assertEqual(None, parsed.twitter_key)
        self.assertEqual(None, parsed.twitter_secret)
        self.assertEqual(None, parsed.log_file)
        self.assertEqual(False, parsed.just_get_status)
        self.assertEqual(False, parsed.debug)

#    def test_charge_curent_high(self):
#        parsed = argparser.init(["-ch", ])
#        self.assertEqual(30.0, parsed.charge_current_high)
#
#        parsed = argparser.init(["-ch", "10.0"])
#        self.assertEqual(10.0, parsed.charge_current_high)
#
#        parsed = argparser.init(["--charge-current-high", "20.0"])
#        self.assertEqual(20.0, parsed.charge_current_high)


if __name__ == "__main__":
    unittest.main()
