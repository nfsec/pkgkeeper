#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
title: PKGkeeper
description: A script to manage package hold states on Debian-based systems.
author: Patryk 'agresor' Krawaczyński (NFsec.pl)
version: 2.0
date: 2025-10-20
license: Apache-2.0

usage: ./pkgkeeper.py [package_name1 package_name2 ...]
       ./pkgkeeper.py (clear all holds by providing no arguments)
"""
import sys
import subprocess

def error(message):
    """
    Print the error message and exit with a status of 1.
    """
    print("ERROR: " + message)
    sys.exit(1)


def check_package(package):
    """
    Make sure the package is installed on the system before you mark it.
    """
    try:
        result = subprocess.run(["dpkg-query", "-W", "-f=${Status}", package],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True)
        if "ok installed" in result.stdout:
            return True
        else:
            return False
    except Exception as e:
        error(str(e))


def new_markers():
    """
    Read the names of the packages from the script arguments and create a set of them.
    """
    new_package_markers = set()
    for x in sys.argv[1:]:
        if check_package(x):
            new_package_markers.add(x)
        else:
            error(f"Package {x} not installed in system. Can't mark it.")
    return new_package_markers


def old_markers():
    """
    Read the names of the packages from the existing 'hold list' and create a set of them.
    """
    try:
        show_hold = (subprocess.check_output("apt-mark showhold", stderr=subprocess.STDOUT, shell=True,
                                            universal_newlines=True).splitlines())
        old_package_markers = set(show_hold)
        return old_package_markers
    except Exception as e:
        error(str(e))

def compare_markers(old_packages, new_packages):
    """
    Compare the two sets and provide a list of information on which packages should be added or removed.
    """
    try:
        if new_packages == old_packages:
            sys.exit(0)
        else:
            add_packages = new_packages.difference(old_packages)
            remove_packages = old_packages.difference(new_packages)
            return list(add_packages), list(remove_packages)
    except Exception as e:
        error(str(e))


def add_markers(*args):
    """
    Put the new packages in the 'hold' state.
    """
    for arg in args:
        try:
            subprocess.run(["apt-mark", "hold", arg], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            error(str(e))


def del_markers(*args):
    """
    Remove any packages that are no longer needed from the 'hold' state.
    """
    for arg in args:
        try:
            subprocess.run(["apt-mark", "unhold", arg], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            error(str(e))


if __name__ == "__main__":
    new = new_markers()
    old = old_markers()
    add, remove = compare_markers(old, new)
    add_markers(*add)
    del_markers(*remove)
