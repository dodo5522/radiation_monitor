#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
TS-MPPT-60 monitor application's hook library.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import subprocess
import logging
import xively


class EventHandler(object):
    """ Event handeler abstract class. """

    _FORMAT_LOG_MSG = "%(asctime)s %(name)s %(levelname)s: %(message)s"
    _FORMAT_LOG_DATE = "%Y/%m/%d %p %l:%M:%S"

    def __init__(self, log_file_path=None, debug=False):
        self._init_logger(log_file_path, debug)

    def _init_logger(self, log_file_path, debug):
        self.logger = logging.getLogger(type(self).__name__)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt=self._FORMAT_LOG_MSG, datefmt=self._FORMAT_LOG_DATE)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        if log_file_path:
            handler = logging.FileHandler(log_file_path, mode="a")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

    def run_handler(self, *args, **kwargs):
        raise NotImplementedError


class XivelyEventHandler(EventHandler):
    def __init__(
            self, log_file_path=None, debug=False,
            api_key=None, feed_key=None):
        EventHandler.__init__(self, log_file_path, debug)
        self._api_key = api_key
        self._feed_key = feed_key

    def run_handler(self, datastreams, **kwargs):
        """ Update xively feed with datastreams.

        Keyword arguments:
            datastreams: list of xively.Datastream object
        """
        api = xively.XivelyAPIClient(self._api_key)
        feed = api.feeds.get(self._feed_key)

        feed.datastreams = datastreams
        feed.update()


class BatteryEventHandler(EventHandler):
    EDGE_NONE = 0
    EDGE_RISING = 1
    EDGE_FALLING = 2

    def __init__(
            self, log_file_path=None, debug=False,
            cmd="/tmp/remote_shutdown.sh",
            target_edge=EDGE_FALLING,
            target_volt=12.0):
        EventHandler.__init__(self, log_file_path, debug)

        self._cmd = cmd
        self._target_volt = target_volt
        self._target_edge = target_edge
        self.__pre_battery_volt = None

    def _is_battery_edge_condition(
            self, cur_volt, prev_volt, target_volt, target_edge):
        """ Check if the condition of target.

        Keyword arguments:
            cur_volt: current voltage of battery
            target_volt: target (threshold) voltage of battery
            target_edge: falling or rising target_edge

        Returns: True if condition is matched
        """
        if prev_volt is None:
            return False

        if cur_volt < prev_volt:
            cur_edge = self.EDGE_FALLING
        elif cur_volt > prev_volt:
            cur_edge = self.EDGE_RISING
        else:
            cur_edge = self.EDGE_NONE

        self.logger.debug("cur_volt: " + str(cur_volt))
        self.logger.debug("prev_volt: " + str(prev_volt))
        self.logger.debug("cur_edge: " + str(cur_edge))
        self.logger.debug("target_edge: " + str(target_edge))

        condition = False

        if target_edge is self.EDGE_RISING:
            if cur_edge is self.EDGE_RISING:
                if cur_volt > target_volt:
                    condition = True
        elif target_edge is self.EDGE_FALLING:
            if cur_edge is self.EDGE_FALLING:
                if cur_volt < target_volt:
                    condition = True

        return condition

    def run_handler(self, datastreams, **kwargs):
        """ Hook battery charge and run some command according to it.

        Keyword arguments:
            datastreams: list of xively.Datastream object
        """
        for datastream in datastreams:
            if datastream._data["id"] == "BatteryVoltage":
                current_battery_volt = float(datastream._data["current_value"])

                if self.__pre_battery_volt is None:
                    self.__pre_battery_volt = current_battery_volt

                break
        else:
            return

        if self._is_battery_edge_condition(
                current_battery_volt,
                self.__pre_battery_volt,
                self._target_volt,
                self._target_edge) is False:
            self.__pre_battery_volt = current_battery_volt
            return

        proc = subprocess.Popen(
            self._cmd.split(),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_data, stderr_data = proc.communicate()

        self.logger.info(
            "{} is executed and returned below values.".format(self._cmd))
        self.logger.info(stdout_data)
