#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: Glaukon Ariston
# Date: 04.11.2020
# Abstract:
#   Mask the file content

import sys
import os
import mmap


def mask(a, mask):
    return (a ^ mask, a ^ mask)


def unmask(a, mask):
    return (a ^ mask, a)


def maskfile(filepath, seed, op):
    seed = seed.to_bytes(1, sys.byteorder)[0]
    with open(filepath, "rb+") as f:
        # memory-map the file, size 0 means whole file
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as fmap:
            with open(filepath+'.masked', "wb+") as g:
                with mmap.mmap(g.fileno(), length=fmap.size(), access=mmap.ACCESS_WRITE) as gmap:
                    for i in range(fmap.size()):
                        pos = (i%256).to_bytes(1, sys.byteorder)[0]
                        gmap[i], seed = op(fmap[i], seed ^ pos)


def main():
    maskfile(path, seed, mask)
    maskfile(path, seed, unmask)


if __name__ == '__main__':
    main()

