#!/usr/bin/python3

# Copyright (C) 2018 LeoAttn
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import argparse
import datetime
import re
import csv
from collections import OrderedDict


# ------------- Fonctions -------------
def listHosts(text):
    hostsList = []
    regex = re.findall(r"" + regexTemp + "($|[^\d])", text, re.DOTALL)
    if regex:
        for addr in regex:
            hostsList.append(addr[0])
        return hostsList
    else:
        return []


# --------------- Main ----------------
VERSION = "1.0"
# Regex for shell commands
regexDevices = r"^[/a-z]+"
regexTemp = r"^194 \w+\s+0x\d+\s+\d+\s+\d+\s+\d+\s+\w+\s+\w+\s+\S+\s+(\d+)(?:\s[\(][^)]*[\)])?$"
regexMode = r"^(?:^Power mode is:\s+|^Device is in )(\w+)"

# Parse arguments
parser = argparse.ArgumentParser(description='Monitoring HDD and SDD temperatures')
parser.add_argument('-d', '--directory', help='Directory where the CSV file will be save', default='./')
parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + VERSION)
args = parser.parse_args()

if not os.path.isdir(args.directory):
    print("Directory is not valid")
    exit(5)

# Find the list of all devices
cmdDevices = os.popen("/usr/sbin/smartctl -n standby --scan").read()
devices = re.findall(regexDevices, cmdDevices, re.MULTILINE)

# Find the mode and the temperature for each device
for device in devices:
    date = datetime.datetime.now()

    cmdAttr = os.popen("/usr/sbin/smartctl -A " + device).read()
    cmdInfo = os.popen("/usr/sbin/smartctl -n standby -i " + device).read()

    temperature = re.search(regexTemp, cmdAttr, re.MULTILINE).group(1)
    mode = re.search(regexMode, cmdInfo, re.MULTILINE).group(1)

    temperature = int(temperature) if temperature else "Error"
    mode = mode if mode else "Error"

    # Define CSV path
    # dateFormated = date.strftime('%d-%m-%y')

    csvFilename = 'hdd-temp_' + device.replace('/dev/', '') + '.csv'
    if args.directory:
        csvPath = args.directory + '/' + csvFilename
    else:
        csvPath = csvFilename

    createHeader = not os.path.exists(csvPath)

    # Write the result in CSV file
    with open(csvPath, 'a') as csvFile:
        # Add a header if it's a new file
        if createHeader:
            header = OrderedDict([('Date', None), ('Power Mode', None), ('Temperature', None)])
            dw = csv.DictWriter(csvFile, delimiter='\t', fieldnames=header)
            dw.writeheader()

        wr = csv.writer(csvFile, quoting=csv.QUOTE_ALL, delimiter=';')
        wr.writerow([date, mode, temperature])

    print("Add row in " + csvPath)


print("Found " + str(len(devices)) + " devices.")
