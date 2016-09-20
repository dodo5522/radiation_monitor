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


def main_routine():
    args = argparser.init()
    logger.configure(path_file=args.log_file, is_debug=args.debug)

    if args.just_get_status:
        exit()

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
        rawdata["data"] = data    # { "Count Per Minute": { "value": 30, "unit": "cpm" }, "Micro Sievert Per Hour": { "value": 0.24, "unit": "usv" }, }
        rawdata["at"] = date_time

        for key, val in data.items():
            logger.info("{date}: {label}: {value}[{unit}]".format(
                date=date_time, label=key, value=str(val["value"]), unit=val["unit"]))

        triggers.put(rawdata)

    geiger_meter = GeigerMeter(
        name="Sparkfun SEN-11345",
        uart_dev=args.serial_device_path[0],
        uart_baud=args.serial_baudrate[0],
        callback_to_get_val=put_to_triggers,
        usv_per_cpm=0.00812)

    geiger_meter.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        logger.info("Monitor program is terminated by user.")
        raise
    except:
        e = sys.exc_info()
        logger.error("Another exception: " + str(e[0]) + " is raised.")
        raise
    finally:
        geiger_meter.stop()
        geiger_meter.join()
        triggers.stop()

main_routine()
