#!/usr/bin/env python

'''
Created on Aug 24, 2012

@author: yhyan
'''

import os
import string

from fabric.api import local, sudo, put, run
from fabric.context_managers import cd

from fabriclib import connect_host, ensure_remote_dir, ensure_remote_file
from utils import PROJECT_DIR, safe_exit, get_settings, get_server_conf

__all__ = ["get_processor"]

class BaseCommand():
    def __init__(self, command, options):
        self.command = command
        self.options = options
        self.settings = get_settings()    
                
        if not self.settings.has_key("PROJECT_NAME") or not self.settings.get("PROJECT_NAME"):
            safe_exit("You must specify PROJECT_NAME in your settings file.\n", 1)
        
        self.PROJECT_NAME = self.settings.get("PROJECT_NAME")
        
        self.AVAILABLE_DIR = self.settings.get("AVAILABLE_DIR", "/var/%s/available"%(self.PROJECT_NAME))
        self.ENABLED_DIR = self.settings.get("ENABLED_DIR", "/var/%s/enabled"%(self.PROJECT_NAME))
        self.LOG_DIR = self.settings.get("LOG_DIR", "/var/%s/log"%(self.PROJECT_NAME))
        self.DATA_DIR = self.settings.get("DATA_DIR", "/var/%s/data"%(self.PROJECT_NAME))
        
    def _get_version_list(self, app, dir_name): # dir_name is 'source' or 'conf'
        l = sudo("ls %s"%(os.path.join(self.AVAILABLE_DIR, app, dir_name))).split()
        l.sort()    
        return l
    
    def _get_current_version_number(self, app, dir_name):
        l = self._get_version_list(app, dir_name)
        return None if not l else l[-1]

    def _get_next_version_number(self, app, dir_name):
        l = self._get_version_list(app, dir_name)    
        return "000000" if not l else "%06d"%(int(l[-1]) + 1)

    def _get_previous_version_number(self, app, dir_name, x=1):
        l = self._get_version_list(app, dir_name)
        i = len(l) - 1 - x
        return l[i] if i >= 0 else None
               
    def execute(self, dest, server, app):
        connect_host(dest, server)
        
        for dir in [self.AVAILABLE_DIR, self.ENABLED_DIR, self.LOG_DIR, self.DATA_DIR]:
            ensure_remote_dir(dir, "root", "777")
            
        return self.doit(dest, server, app)
    
    def doit(self, dest, server, app):
        raise NotImplementedError, "You should implemente this function in child class."    

class DeployCommand(BaseCommand):
    def deploy(self, dest, server, app, dir_name):  # dir_name is a sub directory of app. eg. source, conf .    
        ensure_remote_dir(os.path.join(self.AVAILABLE_DIR, app, dir_name))
        version = self._get_next_version_number(app, dir_name)
        available = os.path.join(self.AVAILABLE_DIR, app, dir_name, version)
        enabled = os.path.join(self.ENABLED_DIR, app)
        ensure_remote_dir(available)
        ensure_remote_dir(enabled)
        
        if dir_name == "source":
            local("cd %s; tar cvzf /tmp/%s.tar.gz --exclude='.svn' ./%s;"%(os.path.join(PROJECT_DIR, app), dir_name, dir_name))
        elif dir_name == "conf":
            local("cd %s; tar cvzf /tmp/%s.tar.gz --exclude='.svn' ./%s;"%
                  (os.path.join("/tmp/", self.PROJECT_NAME, dest, server, app), dir_name, dir_name))
        else:
            safe_exit("Not support dir_name.\n")
              
        put("/tmp/%s.tar.gz"%(dir_name), available)
        with cd(available):
            run("tar zvxf %s.tar.gz"%(dir_name))
            run("rm -f %s"%(os.path.join(enabled, dir_name)))
            run("ln -s %s %s"%(os.path.join(available, dir_name), os.path.join(enabled, dir_name)))
    
    def get_conf(self, dest, server, app):
        tmp_dir = os.path.join("/tmp/", self.PROJECT_NAME, dest, server, app)
        tmp_conf_dir = os.path.join(tmp_dir, "conf")
        os.system("rm -f -r %s"%(tmp_conf_dir))
        os.system("mkdir -p %s"%(tmp_conf_dir))
        conf_dir = os.path.join(PROJECT_DIR, app, "conf") 
        vars = get_server_conf(dest, server)
        for s in os.listdir(conf_dir):
            abs_path_temp = os.path.join(conf_dir, s)
            if os.path.isfile(abs_path_temp) :
                content = None
                with open(abs_path_temp, "r") as fp:
                    content = "".join(fp.readlines())
                config_content = content % vars
                with open(os.path.join(tmp_conf_dir, s), "w") as fp:
                    fp.write(config_content)
    
    def doit(self, dest, server, app):
        if self.options.dir_name == "source":
            self.deploy(dest, server, app, "source")
        elif self.options.dir_name == "conf":
            self.get_conf(dest, server, app)
            if not self.options.debug:
                self.deploy(dest, server, app, "conf") 
        else:
            safe_exit("Not support dir_name.\n")
             
class RollbackCommand(BaseCommand):
    def doit(self, dest, server, app):   
        dir_name = self.options.dir_name  # dir_name = "source" or "conf"
        if dir_name not in ["source", "conf"]:
            safe_exit("Not support dir_name.\n")
        
        ensure_remote_dir(os.path.join(self.AVAILABLE_DIR, app, dir_name))
        current_version = self._get_current_version_number(app, dir_name)
        version = self._get_previous_version_number(app, dir_name)
        
        if not version:
            safe_exit("%s %s %s %s version number error.\n"%(dest, server, app, dir_name), 1)
        
        available = os.path.join(self.AVAILABLE_DIR, app, dir_name, version)
        enabled = os.path.join(self.ENABLED_DIR, app)
        
        run("rm -f %s"%(os.path.join(enabled, dir_name)))
        run("ln -s %s %s"%(os.path.join(available, dir_name), os.path.join(enabled, dir_name)))
        run("rm -r %s"%(os.path.join(self.AVAILABLE_DIR, app, dir_name, current_version)))
    
class UserCommand(BaseCommand):
    def get_script_path(self):
        return reduce(lambda x, y: os.path.join(x, y), self.command.split("."), "")
    
    def doit(self, dest, server, app):
        SUB_DIR = "scripts"
        real = os.path.join(self.AVAILABLE_DIR, app, SUB_DIR)
        symb = os.path.join(self.ENABLED_DIR, app, SUB_DIR)
        run("mkdir -p %s"%(real))
        
        ensure_remote_dir(os.path.dirname(symb))
        run("if [ ! -h %s ]; then rm -rf %s; ln -s %s %s; fi"%(symb, symb, real, symb))
        
        script_path = self.get_script_path() 
        local_script_path = os.path.join(PROJECT_DIR, app, SUB_DIR, script_path)
        remote_script_path = os.path.join(real, script_path)
        
        ensure_remote_dir(os.path.dirname(remote_script_path))
        
        if self.options.force:
            put(local_script_path, remote_script_path)
        else:
            ensure_remote_file(local_script_path, remote_script_path)
            
        run("chmod +x %s; %s"%(remote_script_path, remote_script_path))

class UploadCommand(BaseCommand):
    def doit(self, dest, server, app):
        SUB_DIR = "files"
        
        real = os.path.join(self.AVAILABLE_DIR, app, SUB_DIR)
        symb = os.path.join(self.ENABLED_DIR, app, SUB_DIR)
        run("mkdir -p %s"%(real))
        
        ensure_remote_dir(os.path.dirname(symb))
        run("if [ ! -h %s ]; then rm -rf %s; ln -s %s %s; fi"%(symb, symb, real, symb))
        
        file_dir = os.path.join(PROJECT_DIR, app, SUB_DIR)
        abs_file_path = os.path.join(file_dir, self.options.file)
        if os.path.isfile(abs_file_path):
            ensure_remote_file(abs_file_path, os.path.join(real, self.options.file))

def get_processor(command, options):
    if command == "deploy":
        return DeployCommand(command, options)
    elif command == "rollback":
        return RollbackCommand(command, options)
    elif command == "upload":
        return UploadCommand(command, options)
    else:
        return UserCommand(command, options)
        