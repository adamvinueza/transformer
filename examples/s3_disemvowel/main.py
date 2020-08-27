#!/usr/bin/env python
import s3fs
from transformer.transform import Transform
from disemvowel import disemvowel

if __name__ == '__main__':
    fs = s3fs.S3FileSystem(anon=False)
    tr = Transform(fs=fs, overwrite=True)
    src = "s3://test-transform-in/banana.txt"
    dest = "s3://test-transform-out/bnn.txt"
    tr(src, dest, disemvowel, [])
    with fs.open(dest, 'r') as rdr:
        for line in rdr.readline():
            for c in line:
                assert(c.lower() not in 'aeiou')
