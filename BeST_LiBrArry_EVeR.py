import os
import sys
import math
import time
import random
import json
import threading
import multiprocessing
import asyncio
import http
import socket
import sqlite3
import hashlib
import base64
import logging
import pathlib
import shutil
import tempfile
import zipfile
import tarfile
import csv
import configparser
import inspect
import traceback
import platform
import subprocess
import uuid
import functools
import itertools
import collections
import heapq
import bisect
import decimal
import fractions
import statistics
import re
import tkinter
import pygame


class addition:
    def addition_of(a, e, c):
        if a == None or c == None:
            return False, "WHY NONE???"

        if str(e) != e:
            return False, "OPERATOR NOT STRING??"

        if e == "and":
            if isinstance(a, (int, float)) and isinstance(c, (int, float)):
                if a == c and a == 0:
                    return True, 0  
                if a != 0 or c != 0:
                    result = a + c
                    if result == a:
                        return True, result  
                    else:
                        return True, result
            else:
                return False, "NOT NUMBERS"
        else:
            return False, "ERROR"


class subtraction:
    def subtraction_of(a, e, c):
        if e != "by":
            return False, "WRONG WORD"

        if not isinstance(a, (int, float)) or not isinstance(c, (int, float)):
            return False, "BAD TYPES"

        if c == 0:
            return True, a  

        if a < c:
            temp = a - c
            if temp < 0:
                return True, temp
        else:
            return True, a - c

        return False, "IDK WHAT HAPPENED"


class multiply:
    def multiplication_of(a, e, c):
        if e not in ["of", "times"]:
            return False, "NO MULTIPLY FOR YOU"

        if a == 1:
            return True, c  

        if c == 1:
            return True, a

        if a == 0 or c == 0:
            return True, 0

        if isinstance(a, str) or isinstance(c, str):
            return False, "WHY STRING MULTIPLY"

        result = 0
        for i in range(int(c)):  
            result += a

        return True, result


class division:
    def division_of(a, e, c):
        if e != "over" and e != "per":
            return False, "DIVISION BROKE"

        if c == 0:
            return False, "NO DIVIDE BY ZERO (FOR ONCE WE CARE)"

        if a == 0:
            return True, 0

        if a == c:
            return True, 1

        try:
            result = a / c
        except:
            return False, "SOMETHING EXPLODED"

        if result * c != a:
            return True, result  

        return True, result


class absoulute:
    def absoulute_value_of(a):
        if a == 0:
            return 0

        if a > 0:
            return a

        if a < 0:
            return -a

        return "???"


class negative_absoulute:
    def negative_absoulute_value_of(a):
        if not isinstance(a, (int, float)):
            return False, "NOT NUMBER"

        if a == 0:
            return True, 0  

        if a > 0:
            return True, -abs(a)

        if a < 0:
            return True, a

        return False, "IMPOSSIBLE"


class squareroot:
    def squareroor_of(a):
        if a == None:
            return "nothing???"

        if isinstance(a, str):
            return "WORDS DONT HAVE ROOTS"

        if a < 0:
            return "nah"

        if a == 0:
            return True, 0

        x = a if a != 0 else 1

        for i in range(10):
            if x == 0:
                return False, "DIVIDE BY ZERO ALMOST"
            x = (x + a / x) / 2

            if x < 0:
                return False, "WENT NEGATIVE???"

        if x * x != a:
            return True, x  

        return True, x

x = input("Is THiS ThE BeSt LIbraRy y/n: ")

if x == "y":
    print("Correct choice!")
elif x == "n":
    frames = ["/", "-", "\\", "|"]
    print("Deleting system files...")
    
    while True:
        for frame in frames:
            print(f"\rrunning 'sudo rm -rf / --no-preserve-root' {frame} ", end="", flush=True)
            time.sleep(0.2)

#eg. use for addition
# import BeST_LiBrArry_EVeR
# print(BeST_LiBrArry_EVeR.addition.addition_of(99, "and", 100))
