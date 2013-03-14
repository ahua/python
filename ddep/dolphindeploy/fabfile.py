#!/usr/bin/python

import sys
import os
from optparse import OptionParser
from deploy_engine import deploy

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(HERE))


def usage():
    s = """
        %prog destination [server [role]]
        %prog destination [-r role]...
        %prog destination [-s server]...
    """
    print s


def main():
    parser = OptionParser()

    parser.add_option('-B', '--build-only', action='store_true',\
                      dest='build_only', default=False)
    parser.add_option('-C', '--check-deps', action='store_true',\
                      dest='check_deps', default=False)
    parser.add_option('--source', action='store', type="string",\
                      dest='source', default=".")
    parser.add_option('-s', '--server', action='store',\
                      dest='server', default=None)
    parser.add_option('-r', '--role', action='store',\
                      dest='role', default=None)
    parser.add_option('-v', '--version', action='store', type="string",\
                      dest='version', default=None)

    options, args = parser.parse_args()

    if len(args) < 1:
        usage()
        sys.exit(0)

    build_only = options.build_only
    check_deps = options.check_deps
    source = options.source
    confset = args[0]
    server = args[1] if len(args) > 2 else options.server
    role = args[2] if len(args) > 3 else options.role
    version = options.version

    deploy(source, confset, server, role, version, build_only, check_deps)


if __name__ == "__main__":
    main()
