#!/usr/bin/env python

'''
Created on Aug 24, 2012

@author: yhyan
'''

import os
import sys
import ConfigParser
import importlib

__all__ = ["PROJECT_DIR", "CONF_DIR", "get_config", "safe_exit", "get_settings", "get_server_conf"]

PROJECT_DIR = os.getcwd()
CONF_DIR = os.path.join(PROJECT_DIR, "conf")

_SETTINGS = {}
_MODULE_FILE = None
def get_settings(dir_path=CONF_DIR, module="settings"):
    global _SETTINGS, _MODULE_FILE
    
    module_file = os.path.join(dir_path, module+".py")
    if _SETTINGS and module_file == _MODULE_FILE:
        return _SETTINGS
    
    fp = os.path.join(dir_path, module + ".py")
    if not os.path.exists(fp):
        safe_exit("Please create settings file: %s\n"%fp, 1)
        
    if dir_path not in sys.path:
        sys.path.append(dir_path)
    m = importlib.import_module(module)
    for k in dir(m):
        if not k.startswith("_"):
            _SETTINGS[k] = getattr(m, k)
    os.remove(os.path.join(dir_path, module+".pyc"))

    _MODULE_FILE = fp
    return _SETTINGS

_CONFIG, _DEST = None, None
def get_config(dest=None):
    global _CONFIG, _DEST
    
    if _DEST == dest and _CONFIG:
        return _CONFIG   
    config = ConfigParser.ConfigParser()
    filenames = map(lambda cfg_file: os.path.join(PROJECT_DIR, "conf", dest, cfg_file), 
                    ["common.cfg", "key.cfg"])
    if all(map(lambda fp: os.path.isfile(fp), 
               filenames)):
        config.read(filenames)
    else:
        safe_exit("%s doesn't exist.\n"%filenames)
    _CONFIG, _DEST= config, dest

    return config

def get_server_conf(dest, server):
    config = ConfigParser.ConfigParser()
    config.optionxform = str
    
    filename = os.path.join(PROJECT_DIR, "conf", dest, "vars.cfg")
    
    if not os.path.isfile(filename):
        return {}
    
    config.read([filename])    
    
    ret = {}
    if config.has_section("default"):
        for k, v in config.items("default"):
            ret[k] = v
    if config.has_section(server):
        for k, v in config.items(server):
            ret[k] = v
    return ret

def safe_exit(msg, code=0, fp=sys.stdout):
    if msg:
        fp.write(msg)
    sys.exit(code)

