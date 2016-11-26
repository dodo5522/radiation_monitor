# Status

[![Build Status](https://travis-ci.org/dodo5522/radiation_monitor.svg?branch=master)](https://travis-ci.org/dodo5522/radiation_monitor)
[![Coverage Status](https://coveralls.io/repos/github/dodo5522/radiation_monitor/badge.svg?branch=master)](https://coveralls.io/github/dodo5522/radiation_monitor?branch=master)

# What's this?

This is an application to monitor our geiger counter module.

# How to install

1. Buy Geiger Counter (SEN-11345) and [install firmware modified by me](https://github.com/dodo5522/Geiger_Counter/tree/master/firmware/geiger_counter_board).
1. pip3 install -r requirements.txt
2. pip3 install git+https://github.com/dodo5522/radiation_monitor.git

# How to configure

1. Customize /etc/defaults/radiation_monitor

# Requirement

* keen>=0.3.20
* xively-python>=0.1.0rc1
* pyserial>=3.0.0

## Sequence diagram overall

![](https://raw.githubusercontent.com/dodo5522/radiation_monitor/master/doc/sequence.png)

## Class module structure

![](https://raw.githubusercontent.com/dodo5522/radiation_monitor/master/doc/class.png)

## Database record structure (in future)

![](https://raw.githubusercontent.com/dodo5522/radiation_monitor/master/doc/database.png)
