#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import datetime
import unittest
from radiation_monitor.event.trigger import BatteryFullTrigger
from radiation_monitor.event.handler import IEventHandler
from unittest.mock import MagicMock


class TestBatteryFullTrigger(unittest.TestCase):
    """test BatteryHandler class."""

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

    def test_not_in_condition(self):
        DummyEventHandler = MagicMock(spec=IEventHandler)

        event_trigger = BatteryFullTrigger(full_voltage=25.0)
        hoge_handler = DummyEventHandler()

        event_trigger.append(hoge_handler)
        event_trigger.start()

        expected_data = {
            "at": datetime.datetime.now().isoformat(),
            "data": {
                "Battery Voltage": {
                    "value": 24.0
                }
            }
        }

        event_trigger.put_q(expected_data)
        event_trigger.join_q()

        event_trigger.stop()
        event_trigger.join()

        if sys.version_info[:2] >= (3, 5):
            hoge_handler.put_q.assert_not_called()
            hoge_handler.join_q.assert_not_called()
        else:
            self.assertFalse(hoge_handler.put_q.called)
            self.assertFalse(hoge_handler.join_q.called)

    def test_higher_voltage_than_intialized_one(self):
        DummyEventHandler = MagicMock(spec=IEventHandler)

        event_trigger = BatteryFullTrigger(full_voltage=25.0)
        hoge_handler = DummyEventHandler()

        event_trigger.append(hoge_handler)
        event_trigger.start()

        expected_data = {
            "at": datetime.datetime.now().isoformat(),
            "data": {
                "Battery Voltage": {
                    "value": 25.1
                }
            }
        }

        event_trigger.put_q(expected_data)
        event_trigger.join_q()

        event_trigger.stop()
        event_trigger.join()

        self.assertEqual(hoge_handler.put_q.call_args[0][0]["at"], expected_data["at"])
        self.assertEqual(
            hoge_handler.put_q.call_args[0][0]["data"]["Battery Voltage"]["value"],
            expected_data["data"]["Battery Voltage"]["value"])

    def test_voltage_equals_intialized_one(self):
        DummyEventHandler = MagicMock(spec=IEventHandler)

        event_trigger = BatteryFullTrigger(full_voltage=25.0)
        hoge_handler = DummyEventHandler()

        event_trigger.append(hoge_handler)
        event_trigger.start()

        expected_data = {
            "at": datetime.datetime.now().isoformat(),
            "data": {
                "Battery Voltage": {
                    "value": 25.0
                }
            }
        }

        event_trigger.put_q(expected_data)
        event_trigger.join_q()

        event_trigger.stop()
        event_trigger.join()

        self.assertEqual(hoge_handler.put_q.call_args[0][0]["at"], expected_data["at"])
        self.assertEqual(
            hoge_handler.put_q.call_args[0][0]["data"]["Battery Voltage"]["value"],
            expected_data["data"]["Battery Voltage"]["value"])

    def test_voltage_gets_over_intialized_one_more_than_2times(self):
        """ 閾値を２回以上上回っても、トリガーを発火するのは最初の１回のみ """
        DummyEventHandler = MagicMock(spec=IEventHandler)

        event_trigger = BatteryFullTrigger(full_voltage=25.0)
        hoge_handler = DummyEventHandler()

        event_trigger.append(hoge_handler)
        event_trigger.start()

        expected_data = [
            {
                "at": datetime.datetime.now().isoformat(),
                "data": {
                    "Battery Voltage": {
                        "value": 24.9,
                        "unit": "V"
                    }
                }
            },
            {
                "at": datetime.datetime.now().isoformat(),
                "data": {
                    "Battery Voltage": {
                        "value": 25.1,
                        "unit": "V"
                    }
                }
            },
            {
                "at": datetime.datetime.now().isoformat(),
                "data": {
                    "Battery Voltage": {
                        "value": 25.2,
                        "unit": "V"
                    }
                }
            },
        ]

        for data in expected_data:
            event_trigger.put_q(data)
            event_trigger.join_q()

        event_trigger.stop()
        event_trigger.join()

        self.assertEqual(hoge_handler.put_q.call_args[0][0]["at"], expected_data[-2]["at"])
        self.assertEqual(
            hoge_handler.put_q.call_args[0][0]["data"]["Battery Voltage"]["value"],
            expected_data[-2]["data"]["Battery Voltage"]["value"])


if __name__ == "__main__":
    unittest.main()
