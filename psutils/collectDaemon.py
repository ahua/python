#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#####################################################
# Author: yhuang        
# Email: yhuangcgcl@gmail.com
# Last modified:  2011-11-16
#####################################################

import os
import sys, time, signal, traceback
import threading
import socket

from twisted.internet import defer, protocol, reactor
from twisted.application import service, internet


if sys.platform == "linux2":
    from collectors.linux import *
elif sys.platform == "win32" or sys.platform == "win64":
    from collectors.windows import *

#application = service.Application("collectDaemon")
#udpFactory = internet.UDPClient() 
#internet.UDPClient(port, udpFactory).setServiceParent(application)

COLLECTORS = ['cpu', 'mem', 'disk', 'net']
result = {}
MASTER_IP = 'localhost'
MASTER_PORT = 20001


def daemon():
    if os.fork() != 0:
        sys.exit(0)
    os.setsid()


def get_all_metrics(interval):
    threads = []
    for metric in COLLECTORS:
        mp = Collector(metric, interval)
        mp.start()
        threads.append(mp)
    for t in threads:
        t.join()
    return result #全局变量

class Collector(threading.Thread):
    def __init__(self, name, interval):
        threading.Thread.__init__(self)
        self.name = name
        self.interval = interval
    
    def run(self):
        self.result = {
                  'cpu': lambda: cpu_stat.cpu_stats(self.interval).format_output(),
                  'mem': lambda: mem_stat.mem_stats().format_output(),
                  'disk': lambda: disk_stat.disk_stats(self.interval).format_output(),
                  'net': lambda: net_stat.net_stats(self.interval).format_output(),
                  #'process': lambda: process_stat.process_stats().format_output()
        }[self.name]()
        print self.result,'----------------'
        result[self.name] = self.result
        return list(result)
    

class CollectDaemon():
    def __init__(self, interval, duration):
        self.interval = interval
        self.duration = duration
        
    def start(self):
        pidFile = '/var/tmp/collectDaemon.pid'
        open(pidFile, 'w').write(str(os.getpid()))
        sys.stdout.write(time.ctime(time.time()) + 'collect metric Daemon(PID: %s) Started!' % os.getpid())
        sys.stdout.flush()
        self.run()
        
    def stop(self):
        try:
            pidFile = "/var/tmp/collectDaemon.pid"
            pid = int(open(pidFile, 'r').read())
            os.kill(pid, signal.SIGKILL)
            os.remove(pidFile)
        except Exception, e:
            traceback.print_exc()
            pass
    
    def run(self):
        while True:
            metrics = get_all_metrics(self.interval)
            print metrics
            # create udp connecting to master node
            udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udpsock.sendto(str(metrics), (MASTER_IP, MASTER_PORT))
            udpsock.close()
            time.sleep(self.duration)
            

if __name__ == "__main__":
    #if sys.argv[1] == 'start':
    #    daemon()
    #    CollectDaemon(.1, 60).start()
    #if sys.argv[1] == 'stop':
     #   CollectDaemon(.1, 60).stop()
    CollectDaemon(.1, 60).run()
    
    