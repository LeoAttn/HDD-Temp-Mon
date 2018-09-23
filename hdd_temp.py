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
from csv import DictWriter, QUOTE_ALL, writer
from datetime import datetime
from os import path, popen, listdir
from re import search, findall, MULTILINE, match

# --------------- Main ----------------
VERSION = "1.1"
# Regex for shell commands
regexDevices = r"^[/a-z]+"
regexTemp = r"^194 [\w-]+\s+0x\d+\s+\d+\s+\d+\s+\d+\s+[\w-]+\s+\w+\s+\S+\s+(\d+)(?:\s[\(][^)]*[\)])?$"
regexMode = r"^(?:^Power mode is:\s+|^Device is in )(\w+)"

# Parse arguments
parser = ArgumentParser(description='Monitoring HDD and SDD temperatures')
parser.add_argument('-p', '--path', help='Path of directory where the CSV file will be save', default='./')
parser.add_argument('-d', '--devices', nargs='*', help='Device(s) to monitoring')
parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + VERSION)
args = parser.parse_args()

if not path.isdir(args.path):
    print("Directory is not valid")
    exit(5)

if args.devices:
    devices = args.devices
else:
    # Find the list of all devices
    cmdDevices = popen("/usr/sbin/smartctl -n standby --scan").read()
    devices = findall(regexDevices, cmdDevices, MULTILINE)

# Find the mode and the temperature for each device
for device in devices:
    date = datetime.now()

    cmdAttr = popen("/usr/sbin/smartctl -A " + device).read()
    cmdInfo = popen("/usr/sbin/smartctl -n standby -i " + device).read()

    temperature = search(regexTemp, cmdAttr, MULTILINE)
    mode = search(regexMode, cmdInfo, MULTILINE)

    temperature = int(temperature.group(1)) if temperature else "Error"
    mode = mode.group(1) if mode else "Error"

    # Define CSV path
    # dateFormated = date.strftime('%d-%m-%y')

    csvFilename = 'hdd-temp_' + date.strftime('%b-%y') + '_' + device.replace('/dev/', '') + '.csv'
    csvPath = args.path + '/' + csvFilename

    fileNotExist = not path.exists(csvPath)

    if fileNotExist:
        allFiles = listdir(args.path)
        for file in allFiles:
            if match(r"^hdd-temp_\w+-\d{2}_" + device.replace('/dev/', '') + '.csv$', file):
                print("true " + file)
                with tarfile.open('hdd-temp_' + date.strftime('%b-%y') + '_' + device.replace('/dev/', ''), "w") as tar:
                    tar.add(args.path + '/' + file)

    # Write the result in CSV file
    with open(csvPath, 'a') as csvFile:
        # Add a header if it's a new file
        if fileNotExist:
            header = OrderedDict([('Date', None), ('Power Mode', None), ('Temperature', None)])
            dw = DictWriter(csvFile, delimiter='\t', fieldnames=header)
            dw.writeheader()

        wr = writer(csvFile, quoting=QUOTE_ALL, delimiter=';')
        wr.writerow([date, mode, temperature])

    print("Add row in " + csvPath)

print("Monitor: " + str(len(devices)) + " devices.")
