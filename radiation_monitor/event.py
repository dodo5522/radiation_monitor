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

import requests
from collections import OrderedDict
from event_listener.base import IEventHandler


class SafeCastEventHandler(IEventHandler):
    """ Event handler class to send data to SafeCast.

    Args:
        api_key: API key got from SafeCast web site.
        device_id: Device ID registered to SafeCast.
        q_max: max queue number
    Returns:
        Instance object
    """

    API_URL = "https://api.safecast.org/en-US/measurements"

    def __init__(self, api_key, device_id, q_max=5):
        self.api_key_ = api_key
        self.device_id_ = device_id
        IEventHandler.__init__(self, q_max)

    def _run(self, data):
        """ Procedure to run when data received from trigger thread.

        Args:
            data: Pass to the registered event handlers.
        Raises:
            KeyError: latitude or longitude is missing.
        """
        self.send(
            value=data["data"]["value"],
            unit=data["data"]["unit"],
            at=data["at"],
            device_id=self.device_id_,
            latitude=data["data"]["latitude"],
            longitude=data["data"]["longitude"])

    def send(self, value, unit, at, device_id, latitude, longitude, height="1m", surface="Soil", radiation="Air"):
        """ Send the measured sensor data to SafeCast server.

        Args:
            value: Measured value like 0.1 as float
            unit: Unit like "usv" as string
            at: Captured datetime as datetime object
            device_id: Device ID registered to SafeCast.
            latitude: Latitude of the location of geiger counter.
            longitude: Longitude of the location of geiger counter.
            height: Height from the ground like "1m" as string
            surface: The type of ground like "Soil" as string
            radiation: The type of radiation like "Air" as string
        """
        data = OrderedDict()
        data["utf8"] = "✓"
        data["measurement[value]"] = value
        data["measurement[unit]"] = unit
        data["measurement[captured_at]"] = at.strftime("%d %B %Y, %H:%M:%S")
#       data["measurement[location_name]"] = "埼玉県羽生市大字弥勒周辺"
        data["measurement[latitude]"] = latitude
        data["measurement[longitude]"] = longitude
        data["measurement[device_id]"] = device_id
        data["measurement[height]"] = height
        data["measurement[surface]"] = surface
        data["measurement[radiation]"] = radiation

        requests.post("{}?api_key={}".format(self.API_URL, self.api_key_), data=data)


class SafeCastFixedLocationEventHandler(SafeCastEventHandler):
    """ Event handler class to send data to SafeCast with fixed location
        geiger counter.

    Args:
        api_key: API key got from SafeCast web site.
        device_id: Device ID registered to SafeCast.
        latitude: Latitude of the location of geiger counter.
        longitude: Longitude of the location of geiger counter.
        q_max: max queue number
    Returns:
        Instance object
    """

    def __init__(self, api_key, device_id, latitude, longitude, q_max=5):
        self.latitude_ = latitude
        self.longitude_ = longitude
        SafeCastEventHandler.__init__(self, api_key, device_id, q_max)

    def _run(self, data):
        """ Procedure to run when data received from trigger thread.

        Args:
            data: Pass to the registered event handlers.
        """
        self.send(
            value=data["data"]["value"],
            unit=data["data"]["unit"],
            at=data["at"],
            device_id=self.device_id_,
            latitude=self.latitude_,
            longitude=self.longitude_)
