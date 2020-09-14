#!/usr/bin/env python
from argparse import ArgumentParser
import sys
import s3fs
from transformer.transform import Transform
sys.path.append('..')
from disemvowel import disemvowel # noqa

'''
Sample usage:
    ./main.py s3://src-bucket/src-file s3://dest-bucket/dest-file [-w]
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

    # S3 file system and paths to S3 objects
    fs = s3fs.S3FileSystem(anon=False)

    tr = Transform(src_fs=fs, dest_fs=fs, overwrite=args.overwrite)
    tr(src, dest, disemvowel, [])
    with fs.open(dest, 'r') as rdr:
        for line in rdr:
            for c in line:
                assert(c.lower() not in 'aeiou')
