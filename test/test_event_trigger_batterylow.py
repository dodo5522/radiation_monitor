#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import unittest
import datetime
from solar_monitor.event.trigger import BatteryLowTrigger
from unittest.mock import patch, MagicMock


class TestBatteryLowTrigger(unittest.TestCase):
    """ 親のEventListenerクラスで実施済みテスト以外をテストする """

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
        """  """
        batlow_trigger = BatteryLowTrigger(lowest_voltage=12.0)
        batlow_trigger.run_in_condition_ = MagicMock(spec=lambda x: None)
        batlow_trigger.start()

        expected_data = {
            "at": datetime.datetime.now().isoformat(),
            "data": {
                "Battery Voltage": {
                    "value": 13.0
                }
            }
        }

        batlow_trigger.put_q(expected_data)
        batlow_trigger.stop()
        batlow_trigger.join()

        batlow_trigger.run_in_condition_.assert_not_called()

    def test_low_voltage_from_first_time(self):
        """  """
        batlow_trigger = BatteryLowTrigger(lowest_voltage=12.0)
        batlow_trigger.run_in_condition_ = MagicMock(spec=lambda x: None)
        batlow_trigger.start()

        expected_data = {
            "at": datetime.datetime.now().isoformat(),
            "data": {
                "Battery Voltage": {
                    "value": 11.0
                }
            }
        }

        batlow_trigger.put_q(expected_data)
        batlow_trigger.stop()
        batlow_trigger.join()

        args, _ = batlow_trigger.run_in_condition_.call_args
        got_data = args[0]

        self.assertEqual(expected_data["at"], got_data["at"])
        self.assertEqual(expected_data["data"]["Battery Voltage"]["value"], got_data["data"]["Battery Voltage"]["value"])

    def test_low_voltage_from_second_time(self):
        """  """
        batlow_trigger = BatteryLowTrigger(lowest_voltage=12.0)
        batlow_trigger.run_in_condition_ = MagicMock(spec=lambda x: None)
        batlow_trigger.start()

        first_data = {
            "at": datetime.datetime.now().isoformat(),
            "data": {
                "Battery Voltage": {
                    "value": 12.0
                }
            }
        }
        second_data = {
            "at": datetime.datetime.now().isoformat(),
            "data": {
                "Battery Voltage": {
                    "value": 11.9
                }
            }
        }

        batlow_trigger.put_q(first_data)
        batlow_trigger.put_q(second_data)
        batlow_trigger.stop()
        batlow_trigger.join()

        args, _ = batlow_trigger.run_in_condition_.call_args
        got_data = args[0]

        self.assertEqual(second_data["at"], got_data["at"])
        self.assertEqual(second_data["data"]["Battery Voltage"]["value"], got_data["data"]["Battery Voltage"]["value"])

if __name__ == "__main__":
    unittest.main()
