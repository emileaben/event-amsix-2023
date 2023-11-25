#!/usr/bin/env python
import sys
from collections import Counter

#ix_counts = Counter()

### cut-off for errors in traceroute timestamps
end_ts = 1700740800

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


'''
6527 194.81.236.229 1616372035 True True
6527 194.81.236.229 1616372933 True True
6527 194.81.236.229 1616373825 True True
6527 194.81.236.229 1616374732 True True
'''

with open("suitability.pairs.txt", 'rt') as inf:
    for line in inf:
        line = line.rstrip('\n')
        fields = line.split()
        prb_id = fields[0]
        dst_addr = fields[1]
        if not (prb_id,dst_addr) in rpairs:
            continue
        ans = "|".join( [fields[3], fields[4]] ) # True|True  True|False False|True False|False 
        ts = int( fields[2] )
        ts_bin = ts - ( ts % BIN )
        series.setdefault( ts_bin, {} )
        series[ ts_bin ].setdefault( ans, 0 )
        series[ ts_bin ][ ans ] += 1

tsbin_min = min( series.keys() )
tsbin_max = max( series.keys() )

#infras_ordered = list( map( lambda x: x[0], ix_counts.most_common() ) )

types = ['True|True','True|False','False|True','False|False']

print('#ts ' + " ".join( types ) )
tsnow = tsbin_min
while tsnow <= tsbin_max:
    counts = []
    for ttype in types:
        cnt = 0
        if tsnow in series: 
            if  ttype in series[ tsnow ]:
                cnt = series[ tsnow ][ ttype ]
        counts.append( str( cnt ) )
    if tsnow < end_ts:
        print( tsnow, " ".join( counts ) )
    tsnow += BIN
