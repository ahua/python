#!/usr/bin/env python

from optparse import OptionParser
import os
import sys
import ConfigParser

from deploy import print_version 
from deploy.command import get_processor
from deploy.utils import get_config, safe_exit

def get_server_app(dest, server=None, app=None):
    config = get_config(dest)
    
    res = []
    if not server and not app:
        servers = config.sections()
        for server in servers:
            apps = map(lambda _t: _t.strip().rstrip(), config.get(server, "apps").split(","))
            for app in apps:
                res.append((server, app))
        return res
    
    if server not in config.sections(): 
        safe_exit("server %s not found.\n"%(server), 1)   
    if server and not app:
        apps = map(lambda _t: _t.strip().rstrip(), config.get(server, "apps").split(","))
        for app in apps:
            res.append((server, app))
        return res
    
    apps = map(lambda _t: _t.strip().rstrip(), config.get(server, "apps").split(","))
    if app not in apps: 
        safe_exit("app %s not found.\n"%(app), 1)
    
    return [(server, app)]    
        
# return command and a list of (server, app) 
def do_parse(args):
    parser = OptionParser(usage = "prog [options] command destination [server [app]]")
    
    parser.add_option("-a", "--all", action="store_true", dest="all", default=False)
    parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False)
    parser.add_option("-v", "--version", action="store_true", dest="version", default=False)
    parser.add_option("--force", action="store_true", dest="force", default=False)

    parser.add_option("-t", "--type", dest="dir_name", default="source")
    parser.add_option("-f", "--file", dest="file", default=None)
    
    (options, args) = parser.parse_args(args)
    
    if options.version:
        print_version()
        safe_exit(parser.get_usage())
    
    l = len(args)
    if l < 2 or (l < 4 and not options.all):
        safe_exit(parser.get_usage())
        
    if l >= 4:
        return args[0], options, args[1], get_server_app(args[1], args[2], args[3])
    if l == 3:
        return args[0], options, args[1], get_server_app(args[1], args[2])
    if l == 2:
        return args[0], options, args[1], get_server_app(args[1])
    
if __name__ == "__main__":
    command, options, dest, server_app_list = do_parse(sys.argv[1:])
    p = get_processor(command, options)
    for server, app in server_app_list:
        p.execute(dest, server, app)
        