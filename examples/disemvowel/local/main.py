#!/usr/bin/env python
import sys
sys.path.append('..')
from disemvowel import disemvowel
from fsspec.implementations.local import LocalFileSystem
from transformer.transform import Transform

if __name__ == '__main__':
    # local file system and local files
    fs = LocalFileSystem()
    src = "banana.txt"
    dest = "bnn.txt"

    tr = Transform(fs=fs, overwrite=True)
    tr(src, dest, disemvowel, [])
    with fs.open(dest, 'r') as rdr:
        for line in rdr:
            for c in line:
                assert(c.lower() not in 'aeiou')
