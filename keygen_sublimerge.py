#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @author       bitst0rm
# @target       https://github.com/borysf/Sublimerge

import os
import random
import shutil
import zipfile
import sublime
import sublime_plugin

PLUGIN_NAME = 'Sublimerge 3'
URL_OLD = 'https://sublimerge.com/packages.json'
URL_NEW = 'https://sm3.herokuapp.com/verify.php'
SM3 = __import__(PLUGIN_NAME)


class KeygenSublimergeCommand(sublime_plugin.WindowCommand):
    @classmethod
    def run(cls):
        # Defeat server check
        patch()
        keygen()


def pack(src, dst):
    with zipfile.ZipFile('%s.sublime-package' % (dst), 'w', zipfile.ZIP_DEFLATED) as zfh:
        abs_src = os.path.abspath(src)
        for dirname, _, files in os.walk(src):
            for filename in files:
                absname = os.path.abspath(os.path.join(dirname, filename))
                arcname = absname[len(abs_src) + 1:]
                zfh.write(absname, arcname)


def unpack(src, dst):
    with zipfile.ZipFile('%s.sublime-package' % (src), 'r') as zfh:
        zfh.extractall(dst)


def patch():
    smp = os.path.join(sublime.installed_packages_path(), PLUGIN_NAME)
    path = smp + '.sublime-package'
    if not os.path.isfile(path):
        print('File does not exist: %s' % path)
        return None

    linsp = SM3.core.linsp
    verifyu = linsp.VERIFYU
    if URL_NEW == linsp.b64d(verifyu):
        print('File already patched.')
        return None

    verifyn = linsp.b64e(linsp.b64d(verifyu).replace(URL_OLD, URL_NEW))
    bytes_a = verifyu.encode('utf-8')
    bytes_b = verifyn.encode('utf-8')
    if bytes_a != bytes_b and len(bytes_a) == len(bytes_b):
        src = 'Packages/' + PLUGIN_NAME + '/core/linsp.pyc'
        bytes_old = sublime.load_binary_resource(src)
        bytes_new = bytes_old.replace(bytes_a, bytes_b)
        if bytes_old != bytes_new:
            unpack(smp, smp)
            with open(os.path.join(smp, 'core', 'linsp.pyc'), 'wb') as fhr:
                fhr.write(bytes_new)
            pack(smp, smp)
            shutil.rmtree(smp, ignore_errors=True)
            return True
        print('File already patched.')
    print('File has been raped by chuck borys.')
    return None


def keygen():
    lic = SM3.core.linsp.LInsp()
    # key = lic.r_mk(lic.os_fp(), 'sm3')
    key = '-'.join(''.join('%X' % random.randint(0, 15) for i in range(4)) for i in range(5))
    key += '-' + lic.r_mk(key, 'sm3')
    lic.r_ik(key, False, False)
    print('License file: %s' % lic.r_f3())
    print('License key: %s' % lic.r_rl3())
