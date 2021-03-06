'''
Created on Dec 12, 2011

@author: chzhong
'''
from fabric.state import env
from fabric.network import join_host_strings

def setup_host(cp, server):
    host = cp.get(server, 'dns')
    user = cp.get(server, 'user') if cp.has_option(server, 'user') else None
    port = cp.getint(server, 'port') if cp.has_option(server, 'port') else None
    host_string = join_host_strings(user, host, port) if user or port else host

    env.port = port
    env.host_string = host_string

    password = cp.get(server, 'password') if cp.has_option(server, 'password') else None
    keyfile = cp.get(server, 'keyfile') if cp.has_option(server, 'keyfile') else None
    if password:
        env.password = password
        env.passwords[host_string] = password
    if keyfile:
        env.key_filename = keyfile
