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

-----
### Setup

Install Python 3.6.

Use pip to install dependencies by running the command:

pip install bs4 psutil requests 

##### Before running, set variables in xmrspy.py file.

If using in Windows, set a scheduled task to execute this xmrspy.py script every 5 minute (or more).

Open Task Scheduler, create a new task.  In General tab select 'run whether user is logged on or not',  make sure run with highest priveleges is set (necessary for restarting via Devcon and killing xmr-stak-amd).  Under Triggers tab, create a new trigger, set it to run daily, repeat task every 5 minutes.  In Actions tab, create new action to start a program, program/script is "python.exe", add arguments will be 'C:\location\of\xmrspy.py", start in should be the location that you installed Python3.6 to (for me this is C:\Python36).


#### Donate XMR:
4AoUQNiUoE6EkPoJGDPR5bi8EKv9diZFq5hJi86oKJxxYfxayDzSh8PhwikProAvR8PmF2wxzVArKGL3Xu9GKCdU8xQvACv
