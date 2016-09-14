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

from collections import OrderedDict
from datetime import datetime
import unittest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from radiation_monitor.event import SafeCastEventHandler
from radiation_monitor.event import SafeCastFixedLocationEventHandler


class TestSafeCastEventHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @patch("radiation_monitor.event.requests.post", autospec=True)
    def test_run_with_normal(self, patched_post):
        data = {}
        data["at"] = datetime(2016, 1, 1, 10, 00)
        data["data"] = {
            "value": 0.1,
            "unit": "cpm",
            "latitude": 123.0,
            "longitude": 789.0,
        }
        expected_data = OrderedDict()
        expected_data["utf8"] = "✓"
        expected_data["measurement[value]"] = data["data"]["value"]
        expected_data["measurement[unit]"] = data["data"]["unit"]
        expected_data["measurement[captured_at]"] = data["at"].strftime("%d %B %Y, %H:%M:%S")
#       expected_data["measurement[location_name]"] = "埼玉県羽生市大字弥勒周辺"
        expected_data["measurement[latitude]"] = data["data"]["latitude"]
        expected_data["measurement[longitude]"] = data["data"]["longitude"]
        expected_data["measurement[device_id]"] = 123
        expected_data["measurement[height]"] = "1m"
        expected_data["measurement[surface]"] = "Soil"
        expected_data["measurement[radiation]"] = "Air"

        safecast = SafeCastEventHandler(api_key="hogekey", device_id=123)
        safecast.start()
        safecast.put_q(data)
        safecast.join_q()
        safecast.stop()
        safecast.join()

        patched_post.assert_called_once_with("https://api.safecast.org/en-US/measurements?api_key=hogekey", data=expected_data)


class TestSafeCastFixedLocationEventHandler(unittest.TestCase):
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

    @patch("radiation_monitor.event.requests.post", autospec=True)
    def test_run_with_normal(self, patched_post):
        data = {}
        data["at"] = datetime(2016, 1, 1, 10, 00)
        data["data"] = {
            "value": 0.1,
            "unit": "cpm",
        }
        expected_data = OrderedDict()
        expected_data["utf8"] = "✓"
        expected_data["measurement[value]"] = data["data"]["value"]
        expected_data["measurement[unit]"] = data["data"]["unit"]
        expected_data["measurement[captured_at]"] = data["at"].strftime("%d %B %Y, %H:%M:%S")
#       expected_data["measurement[location_name]"] = "埼玉県羽生市大字弥勒周辺"
        expected_data["measurement[latitude]"] = 123.0
        expected_data["measurement[longitude]"] = 456.0
        expected_data["measurement[device_id]"] = 123
        expected_data["measurement[height]"] = "1m"
        expected_data["measurement[surface]"] = "Soil"
        expected_data["measurement[radiation]"] = "Air"

        safecast = SafeCastFixedLocationEventHandler(api_key="hogekey", device_id=123, latitude=123.0, longitude=456.0)
        safecast.start()
        safecast.put_q(data)
        safecast.join_q()
        safecast.stop()
        safecast.join()

        patched_post.assert_called_once_with("https://api.safecast.org/en-US/measurements?api_key=hogekey", data=expected_data)


if __name__ == "__main__":
    unittest.main()
