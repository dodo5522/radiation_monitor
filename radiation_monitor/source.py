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

import threading
from collections import OrderedDict
from datetime import datetime
from radiation_monitor import logger
from serial import Serial
from serial import SerialException


class GeigerMeter(threading.Thread):
    """ Geiger counter class to measure the space radiation.

    Arguments:
        name: Name string like geiger meter device.
        uart_dev: Path to the device file like "/dev/tty.usb-serial".
        uart_baud: UART baudrate like 9600.
        callback: Callback function object. This object needs to have 3 argument
            to input data. First one is name of the geiger meter device, second
            is radiation value, third is the date and time when the radiation
            value is got. The unit of radiation value is uSv/h if usv_per_cpm
            is set, otherwise cpm.
        usv_per_cpm: Rate of uSv/h.
    """

    def __init__(self, name, uart_dev, uart_baud, callback_to_get_val, usv_per_cpm=0.00812):
        self.name_ = name
        self.uart_ = Serial(uart_dev, uart_baud)
        self.callback_ = callback_to_get_val
        self.usv_per_cpm_ = usv_per_cpm
        self.stop_event_ = threading.Event()

        threading.Thread.__init__(self, name=type(self).__name__)

    def stop(self):
        """ Stop this thread. """
        self.stop_event_.set()
        self.uart_.close()

    def run(self):
        """ Target function of this thread. """

        def wait_for_radiation():
            cpm = int(self.uart_.readline().decode("ascii").split()[0])
            return cpm * self.usv_per_cpm_ if self.usv_per_cpm_ else cpm

        while True:
            try:
                self.callback_(
                    self.name_,
                    OrderedDict({
                        "label": "Space Radiation",
                        "value": wait_for_radiation(),
                        "unit": "usv" if self.usv_per_cpm_ else "cpm"
                    }),
                    datetime.utcnow())
            except SerialException:
                if self.stop_event_.is_set():
                    logger.info("SerialException to stop raised.")
                    break
                logger.error("SerialException raised.")
                raise
            except Exception as e:
                logger.error("{} raised.".format(type(e).__name__))
                raise

        self.uart_.close()
