#!/usr/bin/env python
import sys
from collections import Counter

#ix_counts = Counter()

series = {} # keyed by timestamps at BIN size interval
BIN = 15*60

'''
prb_id dst_addr infra_hit_rate dst_hit_rate
6527 194.81.236.229 96 1.0 1.0
6674 83.136.33.8 96 0.7604166666666666 0.0
6879 202.165.66.5 96 1.0 1.0
6380 185.134.197.94 96 1.0 1.0
'''

rpairs = set() # reliable pairs

with open("reliability.pairs.test.txt",'rt') as inf:
    for line in inf:
        line = line.rstrip('\n')
        fields = line.split()
        if float( fields[3] ) == 1.0 and float( fields[4] ) == 1.0:
            pair = ( fields[0], fields[1] )
            rpairs.add( pair )

with open("infras.pairs.txt", 'rt') as inf:
    for line in inf:
        line = line.rstrip('\n')
        fields = line.split()
        infras = []
        prb_id = fields[0]
        dst_addr = fields[1]
        if not (prb_id, dst_addr) in rpairs:
            continue # not a reliable pair
        ts = int( fields[2] )
        ts_bin = ts - ( ts % BIN )
        series.setdefault( ts_bin, {} )
        if len( fields ) == 5:
            infras = fields[4].split('|')
            for i in infras:
                #ix_counts[ i ] += 1
                series[ ts_bin ].setdefault( i, 0 )
                series[ ts_bin ][ i ] += 1
            
        else:
            #ix_counts[ 'None' ] += 1
            series[ ts_bin ].setdefault('None', 0 )
            series[ ts_bin ]['None'] += 1

tsbin_min = min( series.keys() )
tsbin_max = max( series.keys() )

#infras_ordered = list( map( lambda x: x[0], ix_counts.most_common() ) )


tsnow = tsbin_min
ix_max_counts = {}
while tsnow <= tsbin_max:
    if tsnow in series:
        for infra in series[tsnow].keys():
            if not infra in ix_max_counts:
                ix_max_counts[infra] = series[ tsnow ][ infra ]
            elif ix_max_counts[ infra ] < series[ tsnow ][ infra ]:
                ix_max_counts[infra] = series[ tsnow ][ infra ]
    else:
        print( f"error on {tsnow}" , file=sys.stderr )
    tsnow += BIN

infras_ordered = sorted( ix_max_counts.keys(), key=lambda x: ix_max_counts[ x ], reverse=True )

print('#ts ' + " ".join(infras_ordered) )
tsnow = tsbin_min
while tsnow <= tsbin_max:
    counts = []
    for infra in infras_ordered:
        cnt = 0
        if tsnow in series: 
            if infra in series[ tsnow ]:
                cnt = series[ tsnow ][ infra ]
        counts.append( str( cnt ) )
    print( tsnow, " ".join( counts ) )
    tsnow += BIN
