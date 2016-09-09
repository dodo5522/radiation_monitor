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
from serial import Serial


class GeigerMeter(threading.Thread):
    """ aaa

    Arguments:
        uart_dev: Path to the device file like "/dev/tty.usb-serial".
        uart_baud: UART baudrate like 9600.
        callback: Callback function object. This object needs to have an
            argument to input data. The unit is set to uSv/h if usv_per_cpm is
            set, otherwise it's set to "cpm".
        usv_per_cpm: Rate of uSv/h.

    Raises:
        SerialException: When uart_dev etc. is invalid.
    """

    def __init__(self, uart_dev, uart_baud, callback_to_get_val, usv_per_cpm=0.00812):
        self.uart_ = Serial(uart_dev, uart_baud)
        self.callback_ = callback_to_get_val
        self.usv_per_cpm_ = usv_per_cpm

        self.kill_ = threading.Event()
        self.kill_.clear()

        threading.Thread.__init__(self, name=type(self).__name__)

    def stop(self):
        """ Stop this thread. """
        self.kill_.set()

    def run(self):
        """ Target function of this thread. """

        def wait_for_radiation():
            cpm = int(self.uart_.readline().decode("ascii").split()[0])
            return cpm * self.usv_per_cpm_ if self.usv_per_cpm_ else cpm

        while not self.kill_.is_set():
            try:
                self.callback_(wait_for_radiation())
            except:
                raise


if __name__ == "__main__":
    pass
