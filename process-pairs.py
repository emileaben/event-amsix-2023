#!/usr/bin/env python
import glob
import ujson as json
import arrow

import radix

r = radix.Radix()
r.add("195.66.224.0/22")

files = glob.glob("./pairs/*.jsonf")


def hits_infra( r, hops ):
    for h in hops:
        if 'hop_addr' in h:
            if r.search_best( h['hop_addr'] ):
                infra_hit = True
                return True
    return False

def hits_dst( dst_addr, hops ):    
    for h in reversed( hops ):
        if 'hop_addr' in h:
            if h['hop_addr'] == dst_addr:
                return True
    return False

# read the files
for fname in files:
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
        infra_hit = hits_infra( r, hops )
        dst_hit = hits_dst( dst_addr, hops )

        print(prb_id, dst_addr, ts, infra_hit, dst_hit )
