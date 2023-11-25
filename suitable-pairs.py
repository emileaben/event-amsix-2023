#!/usr/bin/env python
import sys
import arrow

### this sets the 'end' of the test day
end_test_ts = arrow.get('2023-11-22T00:00:00Z').timestamp
## 6527 194.81.236.229 1616372035 True True

this_prb_id = None
this_dst_addr = None
infra_hit = 0
dst_hit = 0
cnt = 0
# suitability.pairs.txt has all observations from prb/dst pairs in a contiguous block of lines
# otherwise this wont work:
with open("suitability.pairs.txt", 'rt') as inf:
    for line in inf:
        line = line.rstrip('\n')
        fields = line.split()
        prb_id = fields[0]
        dst_addr = fields[1]
        ts = int( fields[2] )
        has_infra = fields[3] # saw the infra
        dst_resp  = fields[4] # the destination actually responded
        if ts >= end_test_ts:
            continue

        if this_prb_id == None:
            this_prb_id = prb_id
        if this_dst_addr == None:
            this_dst_addr = dst_addr

        if this_prb_id != prb_id or this_dst_addr != dst_addr:
            # calculate stats for the old pair
            print(this_prb_id, this_dst_addr, cnt, infra_hit*1.0/cnt, dst_hit*1.0/cnt)
            infra_hit = 0
            dst_hit = 0
            cnt = 0

        this_prb_id = prb_id        
        this_dst_addr = dst_addr
        if has_infra == 'True':
            infra_hit += 1
        if dst_resp == 'True':
            dst_hit += 1
        cnt+= 1


print(this_prb_id, this_dst_addr, cnt, infra_hit*1.0/cnt, dst_hit*1.0/cnt)
