#!/usr/bin/python
import urllib2
import json
import sys
import os
import getopt
import re

def download_post(board, post, dir):
    if post.has_key('tim') and post.has_key('ext'):
        print post['tim']
        data = urllib2.urlopen('http://i.4cdn.org/%s/%s%s' % (board, post['tim'], post['ext'])).read()
        with open('%s/%s%s' % (dir, post['tim'], post['ext']), 'wb') as f:
            f.write(data)

def print_usage():
    print "Usage: 4chan_dl.py -u <thread url> -o <output directory>"
    exit(0)

def parse_args(args):
    params = {}
    optlist, args = getopt.getopt(args, '?u:o:')
    for o, a in optlist:
        if o == '-u':
            params['url'] = a
        if o == '-o':
            params['dir'] = a
        if o == '?':
            print_usage()
    return params

params = parse_args(sys.argv[1:])
if not params.has_key('url') or not params.has_key('dir'):
    print_usage()

if not os.path.isdir(params['dir']):
    os.makedirs(params['dir'])

dir = params['dir'].strip('/')
board = re.findall('\.org?/.*?/', params['url'])[0][5:-1]
thrd = re.findall('/thread/[0-9]*/', params['url'])[0][8:-1]
str = urllib2.urlopen('http://a.4cdn.org/' + board + '/thread/' + thrd + '.json').read()
o = json.loads(str)
for post in o['posts']:
    download_post(board, post, dir)

# end of the program

