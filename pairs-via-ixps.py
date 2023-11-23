#!/usr/bin/env python
import requests
import glob
import ujson as json
import arrow
import sys

import radix


def get_ixp_info():
    ix = radix.Radix()
    r_ixpfx = requests.get("https://www.peeringdb.com/api/ixpfx")
    j_ixpfx = r_ixpfx.json()
    for ixpfx in j_ixpfx['data']:
        node = ix.add( ixpfx['prefix'] )
    return ix

ix = get_ixp_info()

files = glob.glob("./pairs/*.jsonf")
series = []

def hits_infra( ix, hops ):
    infra_set = set() # to remove duplicates
    infras = []
    for h in hops:
        if 'hop_addr' in h:
            node = ix.search_best( h['hop_addr'] )
            if node:
                ixpfx = node.prefix
                if not ixpfx in infra_set:
                    infras.append( ixpfx )
                    infra_set.add( ixpfx )
    return infras


def hits_dst( dst_addr, hops ):    
    for h in reversed( hops ):
        if 'hop_addr' in h:
            if h['hop_addr'] == dst_addr:
                return True
    return False

# read the files
i=0
flen = len( files )
for fname in files:
    i += 1
    print("processing fname %s (%s/%s)" % (fname,i,flen), file=sys.stderr )
    series = []
    prb_id = None
    dst_addr = None
    with open(fname, 'rt') as inf:
        for line in inf:
            line = line.rstrip('\n')
            if line == "":
                continue
            try:
                j = json.loads( line )
            except:
                print("+++" + line + "+++")

            if prb_id == None:
                prb_id = j['prb_id']
            if dst_addr == None:
                dst_addr = j['dst_addr']
            ts = arrow.get( j['start_time'], 'YYYY-MM-DD HH:mm:ss ZZZ').timestamp
            series.append( (ts, j['hops'] ) )
    inf.close()

    series = sorted( series, key=lambda x: x[0] )

    for ts,hops in series:
        infras = hits_infra( ix, hops )
        dst_hit = hits_dst( dst_addr, hops )

        print(prb_id, dst_addr, ts, dst_hit, '|'.join(infras) )
