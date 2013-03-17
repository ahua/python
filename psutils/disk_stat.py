#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#####################################################
# Author: yhuang        
# Email: yhuangcgcl@gmail.com
# Last modified:  2011-11-15
#####################################################

import time
import psutil


class disk_stats:
    def __init__(self, interval = 1):
        self.interval = interval
        
    def format_output(self):
        disk_info = psutil.disk_io_counters()

        return {
                'disk_reads': disk_info.read_count,
                'disk_writes': disk_info.write_count,
                'disk_read_bytes': disk_info.read_bytes,
                'disk_write_bytes': disk_info.write_bytes,
        }
     

if __name__ == "__main__":
    disk = disk_stats()
    print disk.format_output()
    