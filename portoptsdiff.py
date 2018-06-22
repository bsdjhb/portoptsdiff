#!/usr/bin/env python2
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
            return data.strip()
        else:
            return None

def formatopt(opt):
    if opt in disopts:
        return '-' + opt
    else:
        return '+' + opt

parser = argparse.ArgumentParser(description='Compare port options')
parser.add_argument('PORTSDIR', nargs='?', default='/usr/ports')
parser.add_argument('PORT_DBDIR', nargs='?', default=None)
args = parser.parse_args()
if not os.path.isdir(os.path.join(args.PORTSDIR, 'Mk')):
    print >> sys.stderr, "%s is not a valid ports tree" % (args.PORTSDIR)
    sys.exit(1)
if not args.PORT_DBDIR:
    args.PORT_DBDIR = makevar(os.path.join(args.PORTSDIR, 'ports-mgmt', 'pkg'), 
                              'PORT_DBDIR')
if not os.path.isdir(args.PORT_DBDIR):
    print >> sys.stderr, "%s is not a ports database directory" % \
        (args.PORT_DBDIR)

stale = []
errors = []
delta = {}
for d in os.listdir(args.PORT_DBDIR):
    if '_' not in d:
        stale.append(d)
        continue
    (category, port) = d.split('_', 1)
    portdir = os.path.join(args.PORTSDIR, category, port)
    portname = category + '/' + port
    if not os.path.isdir(portdir):
        stale.append(portname)
        continue
    defopts = makevar(portdir, 'PORT_OPTIONS', 'PORT_DBDIR=/nonexistent')
    curopts = makevar(portdir, 'PORT_OPTIONS')
    if defopts is None or curopts is None:
        errors.append(portname)
        continue
    defset = set(defopts.split())
    curset = set(curopts.split())
    if defset == curset:
        continue
    disopts = defset - curset
    deltas = sorted(list(curset - defset) + list(disopts))
    delta[portname] = map(formatopt, deltas)

if stale:
    print "Stale options:"
    for p in sorted(stale):
        print '\t', p
if errors:
    print "Unable to parse:"
    for p in sorted(errors):
        print '\t', p
if delta:
    print "Custom options:"
    for p in sorted(delta.keys()):
        print "\t%s: %s" % (p, ", ".join(delta[p]))

    
    
    