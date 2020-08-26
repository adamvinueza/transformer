#!/usr/bin/env python
from transformer.transform import Transform
from disemvowel import disemvowel

if __name__ == '__main__':
    tr = Transform(overwrite=False)
    src = "banana.txt"
    dest = "bnn.txt"
    tr(src, dest, disemvowel, [])
    with open(dest) as rdr:
        for line in rdr:
            for c in line:
                assert(c.lower() not in 'aeiou')
