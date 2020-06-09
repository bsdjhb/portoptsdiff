#!/usr/bin/env python3
#
# Report what port options do not match the defaults.
#
# usage: portsoptdiff [portsdir [dbdir]]

import argparse
import os
import subprocess
import sys

def makevar(path, var, *args):
    with open('/dev/null') as devnull:
        p = subprocess.Popen(['make', '-V', var] + list(args), cwd=path,
                             stderr=devnull, stdout=subprocess.PIPE)
        data = p.communicate()[0]
        if p.returncode == 0:
            return data.decode('utf-8').strip()
        else:
            return None

def parsemoved(portsdir):
    moved = {}
    for line in open(os.path.join(portsdir, 'MOVED')):
        if line.startswith('#'):
            continue
        fields = line.split('|')
        if len(fields) != 4:
            continue
        moved[fields[0]] = fields[1]
    return moved

parser = argparse.ArgumentParser(description='Compare port options')
parser.add_argument('PORTSDIR', nargs='?', default='/usr/ports')
parser.add_argument('PORT_DBDIR', nargs='?', default=None)
args = parser.parse_args()
if not os.path.isdir(os.path.join(args.PORTSDIR, 'Mk')):
    print(args.PORTSDIR, "is not a valid ports tree", file=sys.stderr)
    sys.exit(1)
if not args.PORT_DBDIR:
    args.PORT_DBDIR = makevar(os.path.join(args.PORTSDIR, 'ports-mgmt', 'pkg'), 
                              'PORT_DBDIR')
if not os.path.isdir(args.PORT_DBDIR):
    print(args.PORT_DBDIR, "is not a ports database directory", file=sys.stderr)

stale = []
errors = []
delta = {}
moved = parsemoved(args.PORTSDIR)
movedto = {}
for d in os.listdir(args.PORT_DBDIR):
    if '_' not in d:
        stale.append(d)
        continue
    (category, port) = d.split('_', 1)
    portname = category + '/' + port
    firstname = portname
    while portname in moved and moved[portname]:
        portname = moved[portname]
    portdir = os.path.join(args.PORTSDIR, portname)
    if not os.path.isdir(portdir):
        stale.append(firstname)
        continue
    defopts = makevar(portdir, 'PORT_OPTIONS', 'PORT_DBDIR=/nonexistent',
                      'OPTIONS_NAME=' + d)
    curopts = makevar(portdir, 'PORT_OPTIONS',
                      'PORT_DBDIR=%s' % (args.PORT_DBDIR), 'OPTIONS_NAME=' + d)
    if defopts is None or curopts is None:
        errors.append(firstname)
        continue
    defset = set(defopts.split())
    curset = set(curopts.split())
    if defset == curset:
        continue
    disopts = defset - curset
    deltas = sorted(list(curset - defset) + list(disopts))
    delta[firstname] = list()
    for opt in deltas:
        if opt in disopts:
            delta[firstname].append('-' + opt)
        else:
            delta[firstname].append('+' + opt)
    if (firstname != portname):
        movedto[firstname] = portname

if stale:
    print("Stale options:")
    for p in sorted(stale):
        print("\t%s" % (p))
if errors:
    print("Unable to parse:")
    for p in sorted(errors):
        print("\t%s" % (p))
if delta:
    print("Custom options:")
    for p in sorted(delta.keys()):
        opts = ", ".join(delta[p])
        if p in movedto:
            print("\t%s -> %s: %s" % (p, movedto[p], opts))
        else:
            print("\t%s: %s" % (p, opts))

    
    
    
