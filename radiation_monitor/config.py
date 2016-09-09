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

from event_listener.trigger import DataIsUpdatedTrigger
from event_listener.handler import KeenIoEventHandler
from event_listener.handler import XivelyEventHandler
from event_listener.handler import TweetBotEventHandler


def init_triggers(**kwargs):
    """ Initialize event triggers and handlers according to settings.

    Keyword Args:
        kwargs: see init_args() function to know what option is there.
    Returns:
        list of event triggers which have event hnadlers according to config setting.
    """
    data_updated_trigger = DataIsUpdatedTrigger()

    def get_configs(*configs):
        for conf in configs:
            if not conf:
                return []
        return list(configs)

    configs = get_configs(
        kwargs["keenio_project_id"],
        kwargs["keenio_write_key"])

    if configs:
        data_updated_trigger.append(KeenIoEventHandler(*configs))

    configs = get_configs(
        kwargs["xively_api_key"],
        kwargs["xively_feed_key"])

    if configs:
        data_updated_trigger.append(XivelyEventHandler(*configs))

    configs = get_configs(
        kwargs["twitter_consumer_key"],
        kwargs["twitter_consumer_secret"],
        kwargs["twitter_key"],
        kwargs["twitter_secret"])

    if configs:
        kwconfigs = {}
        kwconfigs["msgs"] = [
            "バッテリ電圧がかなり低下しています。",
            "現在{VALUE}[{UNIT}]ですので、PCサーバ等の電源を落とします。",
            "{YEAR}年{MONTH}月{DAY}日{HOUR}時{MINUTE}分に取得したデータを元にしています。"]
        kwconfigs["value_label"] = "Battery Voltage"

        # remove "battery_limit" member.
        configs.pop(0)
        data_updated_trigger.append(TweetBotEventHandler(*configs, **kwconfigs))

    triggers = []
    if "data_updated_trigger" in locals():
        triggers.append(data_updated_trigger)

    return triggers


if __name__ == "__main__":
    pass
