#!/usr/bin/env python
import sys
import s3fs
from transformer.transform import Transform
sys.path.append('..')
import gpg # noqa

if __name__ == '__main__':
    s3 = s3fs.S3FileSystem(anon=False)
    _ = Transform()
