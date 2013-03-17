#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#####################################################
# Author: yhuang
# Email: yhuangcgcl@gmail.com
# Last modified:  2011-11-15
#####################################################

import time
import psutil


cpu_stat = {}

class cpu_stats:
    def __init__(self, interval = 1):
        self.interval = interval

    def format_output(self):
        cpu_times = psutil.cpu_times()
        return {
                'cpu_user': cpu_times.user, 
                'cpu_system': cpu_times.system,
                'cpu_idle': cpu_times.idle,
               'cpu_percent': psutil.cpu_percent(self.interval)
        }


if __name__ == "__main__":
    cpu = cpu_stats()
    print cpu.format_output()

