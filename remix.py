#!/usr/bin/env python
import json
import sys
import gzip
import glob
from collections import Counter

in_files = glob.glob("./data/*/*.gz")

### TODO counters so we can see if we don't lose data in this step!

fd = None
pair = None
c = Counter()
for fname in in_files:
    with gzip.open(fname, 'r') as inf:
        print(f"processing {fname}")
        for line in inf:
            #line = line.rstrip('\n')
            j = json.loads( line )
            this_pair = ( j['prb_id'], j['dst_addr'] )
            c[ this_pair ] += 1
            if pair != this_pair:
                #print( this_pair )
                # Counter here?
                if fd != None:
                    print("\n", file=fd )
                    fd.close()
                outfname = "./pairs/%s.%s.jsonf" % ( j['prb_id'], j['dst_addr'] )
                fd = open( outfname, 'a' )
            json.dump( j, fd )
            print("\n", file=fd )
            pair = this_pair
print("\n", file=fd )
fd.close()

# counter is quality control
print( "writing a counter for quality control to ./data/.check.remix " )
with open("./data/.check.remix", 'wt' ) as outf:
    json.dump( c.most_common() , outf, indent=2 )
