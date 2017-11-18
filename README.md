# xmr-stak-spy
Python script for monitoring hashrate on XMR-STAK-AMD.


Requirements::

Python 3.6
xmr-stak-amd (http needs to be configured)

OverdriveNTool (profile for GPU needs to be configured)

Devcon tool

Synopsis::

This script can be configured (in Task Scheduler or elsewhere) to run at regular intervals (5 minutes or longer is recommended).

When the script is run it checks localhost:port/h on the xmr-stak-amd webpage, looking for the 60s total number.
It compares this number to the MINIMUM_HASHRATE variable.

If the current hashrate is lower than the MINIMUM_HASHRATE, the following happens:

xmr-stak-amd is killed.

GPUs are disabled / enabled via Devcon.

OverdriveNTool profile settings are applied.

xmr-stak-amd is started.

If the current hashrate is greater than the MINIMUM_HASHRATE, nothing happens.

# Set variables in xmrspy.py file.
