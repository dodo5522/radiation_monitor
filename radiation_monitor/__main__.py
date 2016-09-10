#!/usr/bin/env python3
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

import sys
import time
from radiation_monitor import argparser
from radiation_monitor import config
from radiation_monitor import logger
from radiation_monitor.source import GeigerMeter


args = argparser.init()
logger.configure(path_file=args.log_file, is_debug=args.debug)

if args.just_get_status:
    return

kwargs = dict(args._get_kwargs())
triggers = config.init_triggers(**kwargs)
triggers.start()


def put_to_triggers(device_name, data, date_time):
    """ Monitor charge controller and update database like xively or
        internal database. This method should be called with a timer.

    Args:
        device_name: geiger counter device name
        data: got data
        date_time: date and time when the data is got
    Returns:
        None
    Exceptions:
        queue.Full: If queue of event handler is full
    """
    rawdata = {}
    rawdata["source"] = device_name
    rawdata["data"] = data
    rawdata["at"] = date_time

    for key, datum in data.items():
        logger.info(
            "{date}: {elem}, {value}[{unit}]".format(
                date=date_time, elem=key,
                value=str(data["value"]), unit=data["unit"]))

    triggers.put(rawdata)


geiger_meter = GeigerMeter(
    uart_dev="/dev/tty.Bluetooth-Incoming-Port",
    uart_baud=19200,
    callback_to_get_val=put_to_triggers,
    usv_per_cpm=0.00812)

geiger_meter.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    logger.info("monitor program is terminated by user.")
except:
    e = sys.exc_info()
    logger.error("Another exception: " + str(e[0]) + " is raised.")
finally:
    geiger_meter.stop()
    geiger_meter.join()
    triggers.stop()
