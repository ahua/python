#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#####################################################
# Author: yhuang        
# Email: yhuangcgcl@gmail.com
# Last modified:  2011-11-15
#####################################################

import time
import psutil

ONE_MB = 1024 * 1024.0

class mem_stats:
    def __init__(self, interval = 1):
        self.interval = interval
        
    def format_output(self):
        phy = psutil.phymem_usage()
        virt = psutil.virtmem_usage()
        return {
                'phy_mem_total': phy[0]/ONE_MB,
                'phy_mem_used': phy[1]/ONE_MB,
                'phy_mem_free': phy[2]/ONE_MB,
                'phy_mem_percent': phy[3],
				'virt_mem_total': virt[0]/ONE_MB,
                'virt_mem_used': virt[1]/ONE_MB,
                'virt_mem_free': virt[2]/ONE_MB,
                'virt_mem_percent': virt[3],
        }
     

if __name__ == "__main__":
    mem = mem_stats()
    print mem.format_output()
    