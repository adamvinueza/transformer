#!/usr/bin/env python
import sys
from transformer.transform import Transform
from fsspec.implementations.local import LocalFileSystem
sys.path.append('..')
import gpg # noqa

if __name__ == '__main__':
    local = LocalFileSystem()
    _ = Transform()
