#!/usr/bin/env python
from argparse import ArgumentParser
import sys
sys.path.append('..')
from disemvowel import disemvowel

from fsspec.implementations.local import LocalFileSystem
from transformer.transform import Transform

'''
Sample usage:
    ./main.py banana.txt bnn.txt [-w]
'''
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('src', help="source path")
    parser.add_argument('dest', help="destination path")
    parser.add_argument('--overwrite',
                        '-w',
                        help='write over destination file',
                        action='store_true')

    args = parser.parse_args()
    src = args.src
    dest = args.dest

    # local file system and local files
    fs = LocalFileSystem()

    tr = Transform(fs=fs, overwrite=args.overwrite)
    tr(src, dest, disemvowel, [])
    with fs.open(dest, 'r') as rdr:
        for line in rdr:
            for c in line:
                assert(c.lower() not in 'aeiou')
