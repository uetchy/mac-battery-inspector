#!/usr/bin/env python3

from __future__ import print_function
import subprocess
import re


def getIOReg():
    cmd = "ioreg -l | grep Capacity"
    response = subprocess.check_output(cmd, shell=True)
    return response.decode('utf-8')


def parseIOReg(rawResult):
    maxCapacity = int(re.search(r'"MaxCapacity" = (\d+)\n', rawResult).group(1))
    designCapacity = int(re.search(r'"DesignCapacity" = (\d+)\n', rawResult).group(1))
    cycleCount = int(re.search(r'"Cycle Count"=(\d+)\}', rawResult).group(1))
    return [maxCapacity, designCapacity, cycleCount]


if __name__ == '__main__':
    maxCapacity, designCapacity, cycleCount = parseIOReg(getIOReg())
    print('Max Capacity:', maxCapacity, 'mAh')
    print('Design Capacity:', designCapacity, 'mAh')
    print('Cycle Count:', cycleCount, 'cycles')
    print('Cycle Count Remaining: {} cycles - {}% reached'.format(
        1000 - cycleCount, round(float(cycleCount) / 1000 * 100)))

    availability = float(maxCapacity) / designCapacity
    print('Battery Availability: {}%'.format(round(availability * 100, 1)))

    if (availability < 0.8):
        print(
            '===> Your battery is eligible for free battery replacement service in AppleCare+. Repair it now!'
        )
