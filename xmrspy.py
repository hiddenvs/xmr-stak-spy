import requests
from bs4 import BeautifulSoup
from datetime import datetime
import subprocess
import psutil
import time
import os

"""
xmr-stak-spy

Requirements::

Python 3.6
xmr-stak-amd (http needs to be configured)
OverdriveNTool (profile needs to be configured)
Devcon tool

Synopsis::

This script can be configured (in Task Scheduler or elsewhere) to run at regular intervals (5 minutes or longer is recommended).

When the script is run it checks localhost:port/h on the xmr-stak-amd webpage, looking for the 60s total number.
It compares this number to the MINIMUM_HASHRATE variable (set below).

If the current hashrate is lower than the MINIMUM_HASHRATE, the following happens:
xmr-stak-amd is killed.
GPUs are disabled / enabled via Devcon.
OverdriveNTool profile settings are applied.
xmr-stak-amd is started.

If the current hashrate is greater than the MINIMUM_HASHRATE, nothing happens.

"""


""" Python requires that all forward slashes be escaped.  Use two forward slashes when selecting paths below. """
# Path to logfile - leave "" for no logs.
LOGFILE = ""
# Path to Devcon.exe
PATH_TO_DEVCON = "C:\\Program Files (x86)\\Windows Kits\\10\\Tools\\x64\\devcon.exe"
# Path to the directory that contains xmr-stak-amd
PATH_TO_XMRSTAKAMD_FOLDER = "C:\\Users\\username\\Desktop\\xmr-stak-amd"
# Path to OverdriveNTool.exe
PATH_TO_OVERDRIVENTOOL = "C:\\Users\\username\\Desktop\\OverdriveNTool.exe"
# Path to the profile name in OverdriveNTool that you wish to apply at restart.  Note: One profile will be applied to all GPUs.
OVERDRIVENTOOL_PROFILE_NAME = "Vega"
# GPU numbers as listed in OverdriveNTool.  Should be in a list format, ex. [1] or [1,2,3,4,5,6] or [1,2]
OVERDRIVENTOOL_GPU_NUMBERS = [1,2]
# Minimum desired hashrate.  This script will restart xmr-stak-amd if it goes below this hashrate.
MINIMUM_HASHRATE = 3940
# Port number configured in the xmr-stak-amd config file.  This needs to be configured in xmr-stak-amd for this script to work correctly.
XMR_STAK_AMD_PORT = 8080


def logging(text):
    if LOGFILE is not "":
        timestamp = str(datetime.now())
        with open(LOGFILE, 'a') as logfile:
            logfile.write("[" + timestamp + "] " + text + "\n" )

def killxmrstakamd():
  for proc in psutil.process_iter():
    if proc.name() == "xmr-stak-amd.exe":
      logging("xmr-stak-amd process found.")
      proc.kill()
      logging("Killing process.")


def defcon():
    logging("Disabling GPUs with Devcon: \n" + (subprocess.check_output([PATH_TO_DEVCON, 'disable', 'PCI\VEN_1002&DEV_687F'])).decode('utf-8'))
    time.sleep(5)
    logging("Enabling GPUs with Devcon: \n" + (subprocess.check_output([PATH_TO_DEVCON, 'enable', 'PCI\VEN_1002&DEV_687F'])).decode('utf-8'))
    time.sleep(5)

def applysettings():
    numberofprofiles = len(OVERDRIVENTOOL_GPU_NUMBERS)
    count = 0

    while count < numberofprofiles:
        profile = "-p" + str(OVERDRIVENTOOL_GPU_NUMBERS[count]) + OVERDRIVENTOOL_PROFILE_NAME
        subprocess.call([PATH_TO_OVERDRIVENTOOL, profile])
        logging("Applying OverdriveNTool setting to GPU "+ str(OVERDRIVENTOOL_GPU_NUMBERS[count]))
        count = count + 1
        time.sleep(1)

def startxmramdstak():
    os.chdir(PATH_TO_XMRSTAKAMD_FOLDER)
    logging("Starting xmr-stak-amd")
    subprocess.Popen('xmr-stak-amd.exe')

def restartxmrstakamd():
    killxmrstakamd()
    defcon()
    applysettings()
    startxmramdstak()


try:
    request = requests.get(('http://localhost:' + str(XMR_STAK_AMD_PORT)) +'/h')
    soup = BeautifulSoup(request.text, 'html.parser')


    if request.status_code is 200:
        table_data = [[cell.text for cell in row("td")]
                                 for row in BeautifulSoup(request.text, 'html.parser')("tr")]
        last60 = table_data[5][1]

        logging("Hashrate: %s " % last60)

        if (float(last60) < MINIMUM_HASHRATE):
            logging("Hasrate below minimum.  Restarting xmr-stak-amd.")
            restartxmrstakamd()


    if request.status_code is not 200:
        restartxmrstakamd()

except:
    restartxmrstakamd()
