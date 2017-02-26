#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import unittest
from unittest.mock import MagicMock, patch
from radiation_monitor.__main__ import main_routine


class TestMainRoutine(unittest.TestCase):
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

    @patch("radiation_monitor.argparser")
    @patch("radiation_monitor.config")
    @patch("radiation_monitor.logger")
    @patch("radiation_monitor.source.GeigerMeter")
    def test_exceptions(self, mock_geiger_meter_, mock_logger_, mock_config_, mock_argparser_):
        print(mock_geiger_meter_)
        print(mock_logger_)
        print(mock_config_)
        print(mock_argparser_)
        main_routine()


if __name__ == "__main__":
    unittest.main()
