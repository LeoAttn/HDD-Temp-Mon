```
 _   _ ____  ____      _____                          __  __
| | | |  _ \|  _ \    |_   _|__ _ __ ___  _ __       |  \/  | ___  _ __
| |_| | | | | | | |_____| |/ _ \ '_ ` _ \| '_ \ _____| |\/| |/ _ \| '_ \
|  _  | |_| | |_| |_____| |  __/ | | | | | |_) |_____| |  | | (_) | | | |
|_| |_|____/|____/      |_|\___|_| |_| |_| .__/      |_|  |_|\___/|_| |_|
                                         |_| 
```

# Require

- Python 3
- smartmontools
- privilege execution

# Help

``` sh
usage: hdd_temp.py [-h] [-p PATH] [-d [DEVICES [DEVICES ...]]] [-m] [-v]

Monitoring HDD and SDD temperatures with Python 3

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path of directory where the CSV file will be save
  -d [DEVICES [DEVICES ...]], --devices [DEVICES [DEVICES ...]]
                        Device(s) to monitoring
  -m, --monthly         Split logs monthly
  -v, --version         show program's version number and exit
```

# Licence

```
Copyright (C) 2018 LeoAttn

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```