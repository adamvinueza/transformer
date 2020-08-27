#!/usr/bin/env python
import sys
sys.path.append('..')
from disemvowel import disemvowel

import s3fs
from transformer.transform import Transform

if __name__ == '__main__':
    # S3 file system and paths to S3 objects
    fs = s3fs.S3FileSystem(anon=False)
    src = "s3://test-transform-in/banana.txt"
    dest = "s3://test-transform-out/bnn.txt"

    tr = Transform(fs=fs, overwrite=True)
    tr(src, dest, disemvowel, [])
    with fs.open(dest, 'r') as rdr:
        for line in rdr:
            for c in line:
                assert(c.lower() not in 'aeiou')
