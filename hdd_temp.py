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
import tarfile
from argparse import ArgumentParser
from collections import OrderedDict
import csv
from datetime import datetime
import os
import re

# --------------- Main ----------------
VERSION = "1.2"
# Regex for shell commands
regexDevices = r"^[/a-z]+"
regexTemp = r"^194 [\w-]+\s+0x\d+\s+\d+\s+\d+\s+\d+\s+[\w-]+\s+\w+\s+\S+\s+(\d+)(?:\s[\(][^)]*[\)])?$"
regexMode = r"^(?:^Power mode is:\s+|^Device is in )(\w+)"

# Parse arguments
parser = ArgumentParser(description='Monitoring HDD and SDD temperatures with Python 3')
parser.add_argument('-p', '--path', help='Path of directory where the CSV file will be save', default='./')
parser.add_argument('-d', '--devices', nargs='*', help='Device(s) to monitoring')
parser.add_argument('-m', '--monthly', action='store_true', help='Split logs monthly')
parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + VERSION)
args = parser.parse_args()

if not os.path.isdir(args.path):
    print("Directory is not valid")
    exit(5)

# Define the devices to monitor
if args.devices:
    devices = args.devices
else:
    # Find the list of all devices
    cmdDevices = os.popen("/usr/sbin/smartctl -n standby --scan").read()
    devices = re.findall(regexDevices, cmdDevices, re.MULTILINE)

os.chdir(args.path)

# Find the mode and the temperature for each device
for device in devices:
    date = datetime.now()

    cmdAttr = os.popen("/usr/sbin/smartctl -A " + device).read()
    cmdInfo = os.popen("/usr/sbin/smartctl -n standby -i " + device).read()

    temperature = re.search(regexTemp, cmdAttr, re.MULTILINE)
    mode = re.search(regexMode, cmdInfo, re.MULTILINE)

    temperature = int(temperature.group(1)) if temperature else "Error"
    mode = mode.group(1) if mode else "Error"

    # Define File name
    if args.monthly:
        monthlyDate = date.strftime('%Y-%m') + '_'
    else:
        monthlyDate = ''
    filename = 'hdd-temp_' + monthlyDate + device.replace('/dev/', '')
    csvFilename = filename + '.csv'

    fileNotExist = not os.path.exists(csvFilename)

    # Compress old file if it's a new file and splip logs monthly
    if fileNotExist and args.monthly:
        allFiles = os.listdir('.')
        for file in allFiles:
            if re.match(r"^hdd-temp_\d{4}-\d{2}_" + device.replace('/dev/', '') + '.csv$', file):
                with tarfile.open(file.replace('.csv', '') + '.tar.xz', 'w:xz') as tar:
                    tar.add(file)
                    os.remove(file)
                    print("Compressed file: " + file)

    # Write the result in CSV file
    with open(csvFilename, 'a') as csvFile:
        # Add a header if it's a new file
        if fileNotExist:
            header = OrderedDict([('Date', None), ('Power Mode', None), ('Temperature', None)])
            dw = csv.DictWriter(csvFile, delimiter='\t', fieldnames=header)
            dw.writeheader()

        wr = csv.writer(csvFile, quoting=csv.QUOTE_ALL, delimiter=';')
        wr.writerow([date, mode, temperature])

    print("Add row in " + csvFilename)

print("Monitored devices: " + str(devices))
