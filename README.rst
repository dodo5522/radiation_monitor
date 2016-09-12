Status
======

|Build Status| |Coverage Status|

What's this?
============

This is an application to monitor our geiger counter module.

How to install
==============

1. pip3 install -r requirements.txt
2. pip3 install git+https://github.com/dodo5522/radiation\_monitor.git

How to configure
================

1. Customize /etc/defaults/radiation\_monitor

Requirement
===========

-  keen>=0.3.20
-  xively-python>=0.1.0rc1
-  pyserial>=3.0.0

Sequence diagram overall
------------------------

.. figure:: https://raw.githubusercontent.com/dodo5522/radiation_monitor/master/doc/sequence.png
   :alt: 

Class module structure
----------------------

.. figure:: https://raw.githubusercontent.com/dodo5522/radiation_monitor/master/doc/class.png
   :alt: 

Database record structure (in future)
-------------------------------------

.. figure:: https://raw.githubusercontent.com/dodo5522/radiation_monitor/master/doc/database.png
   :alt: 

.. |Build Status| image:: https://travis-ci.org/dodo5522/radiation_monitor.svg?branch=master
   :target: https://travis-ci.org/dodo5522/radiation_monitor
.. |Coverage Status| image:: https://coveralls.io/repos/github/dodo5522/radiation_monitor/badge.svg?branch=master
   :target: https://coveralls.io/github/dodo5522/radiation_monitor?branch=master
