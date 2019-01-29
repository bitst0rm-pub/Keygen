#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @author       bitst0rm
# @target       https://github.com/20Tauri/DoxyDoxygen

import uuid


def keygen():
    prefix = 'C1'

    def chksum(string):
        result = 0
        for char in string:
            result = result * 31 + ord(char)
        return result


    def generate():
        key = prefix + uuid.uuid4().hex.upper()[:-3]
        num = int(key[-2:], 16) - (chksum(key[:-2]) * 31) % 256

        try:
            char = chr(num)
            if ('0123456789ABCDEF').find(char) != -1:
                return key[:-2] + char + key[-2:]
        except ValueError:
            pass
        return None


    while 1:
        key = generate()
        if key:
            return key


if __name__ == '__main__':
    print('KEY: %s' % keygen())
