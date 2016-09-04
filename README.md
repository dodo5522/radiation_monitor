# Status

[![Build Status](https://travis-ci.org/dodo5522/radiation_monitor.svg?branch=master)](https://travis-ci.org/dodo5522/radiation_monitor)
[![Coverage Status](https://coveralls.io/repos/github/dodo5522/radiation_monitor/badge.svg?branch=master)](https://coveralls.io/github/dodo5522/radiation_monitor?branch=master)

# What is this?

This is an application to monitor solar charger's status ex. TS-MPPT-60.  
The status means... how much power is generated by solar power cells, how much power is charged in battery cells, etc.  

# How to install

1. pip3 install -r requirements.txt
2. pip3 install git+https://github.com/dodo5522/radiation_monitor.git

# How to configure

1. Customize /etc/defaults/radiation_monitor

# Requirement

* Python3
* keen>=0.3.20
* tsmppt60-driver>=0.1.3
* xively-python>=0.1.0rc1

## Sequence diagram overall

![](https://raw.githubusercontent.com/dodo5522/radiation_monitor/master/doc/sequence.png)

## Class module structure

![](https://raw.githubusercontent.com/dodo5522/radiation_monitor/master/doc/class.png)

## Database record structure (in future)

![](https://raw.githubusercontent.com/dodo5522/radiation_monitor/master/doc/database.png)
