#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#####################################################
# Author: yhuang        
# Email: yhuangcgcl@gmail.com
# Last modified:  2011-11-15
#####################################################

import time
import psutil


class net_stats:
    def __init__(self, interval = 1):
        self.interval = interval
        
    def format_output(self):
        net_info = psutil.network_io_counters(pernic=True)
        # print net_info
        res = {}
        for key, value in net_info.items():
            res[key] = {"bytes_sent":value[0],
						"bytes_recv":value[1],
						"packets_sent":value[2],
						"packets_recv":value[3]
						}
        return res
        #return {
        #        'net_bytes_sent': delta[0]/self.interval, # B
        #        'net_bytes_recv': delta[1]/self.interval,
        #        'net_packets_sent': delta[2]/self.interval,
        #        'net_packets_recv': delta[3]/self.interval,
        #}
     

if __name__ == "__main__":
    cpu = net_stats()
    print cpu.format_output()
    