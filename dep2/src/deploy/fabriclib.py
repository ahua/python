'''
Created on Aug 26, 2012

@author: yhyan
'''

import sys

from fabric.api import sudo
from fabric.state import env
from fabric.network import join_host_strings
from fabric.contrib.files import exists
from fabric.operations import put, run

from utils import get_config
from utils import safe_exit

def connect_host(dest, server):
    config = get_config(dest)

    dns = config.get(server, 'dns')
    user = config.get(server, 'user')
    key_filename = config.get(server, 'key_filename') if config.has_option(server, 'key_filename') else None
    password = config.get(server, 'password') if config.has_option(server, 'password') else None
    
    if not key_filename and not password:
        safe_exit("Cann't find key_filename or password in %s %s config file.\n"%(dest, server), 1, sys.stderr)
    
    env.host_string = join_host_strings(user, dns)
    env.password = password
    env.key_filename = key_filename

def ensure_remote_dir(dir, own="common", mode=755):
    if own == "root":
        sudo("mkdir -p -m %s %s" %(mode, dir))
    else:
        run("mkdir -p -m %s %s" %(mode, dir))
    
def ensure_remote_file(abs_local_path, abs_remote_path):
    if not exists(abs_remote_path):
        put(abs_local_path, abs_remote_path)
