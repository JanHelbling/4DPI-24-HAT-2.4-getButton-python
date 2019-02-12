#!/usr/bin/python
# -*- coding: utf-8 -*-
#    button.py
#    Simple function to get Button-pressed for 4DPI-24-HAT 2.4" RaspberryPi Display
#
#    Copyright (C) 2019 by Jan Helbling <jan.helbling@mailbox.org>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import array, fcntl
from time import sleep

_IOC_NRBITS   =  8
_IOC_TYPEBITS =  8
_IOC_SIZEBITS = 14
_IOC_DIRBITS  =  2
_IOC_DIRMASK    = (1 << _IOC_DIRBITS) -1
_IOC_NRMASK     = (1 << _IOC_NRBITS)-1
_IOC_TYPEMASK   = (1 << _IOC_TYPEBITS ) -1
_IOC_NRSHIFT = 0
_IOC_TYPESHIFT = _IOC_NRSHIFT+_IOC_NRBITS
_IOC_SIZESHIFT = _IOC_TYPESHIFT+_IOC_TYPEBITS
_IOC_DIRSHIFT  = _IOC_SIZESHIFT+_IOC_SIZEBITS
_IOC_NONE = 0
_IOC_WRITE = 1
_IOC_READ = 2

def _IOC(dir, type, nr, size):
	ioc = (dir << _IOC_DIRSHIFT ) | (type << _IOC_TYPESHIFT ) | (nr << _IOC_NRSHIFT ) | (size << _IOC_SIZESHIFT)
	if ioc > 2147483647: ioc -= 4294967296
	return ioc

def _IOR(type,nr,size):
	return _IOC(_IOC_READ,  type, nr, size)

LCD4DPI_GET_KEYS = _IOR(ord('K'), 1, 4)
buf = array.array('h',[0])

def getbutton():
	button = 0
	with open('/dev/fb1', 'rw') as fd:
		while True:
			fcntl.ioctl(fd, LCD4DPI_GET_KEYS, buf, 1)
			keys = buf[0]
			if not keys & 0b00001:
				button = 1
				break
			if not keys & 0b00010:
				button = 2
				break
			if not keys & 0b00100:
				button = 3
				break
			if not keys & 0b01000:
				button = 4
				break
			if not keys & 0b10000:
				button = 5
				break
	return button
