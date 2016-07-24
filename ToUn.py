#!/usr/bin/env python3
from ctypes import *
import re
import win32api as w3a
import Locales as lcs
_ToUnicodeEx = WinDLL('user32').ToUnicodeEx
_ToUnicodeEx.argtypes = [c_uint, c_uint, POINTER(c_char), POINTER(c_wchar), c_int, c_uint, c_void_p]
_ToUnicodeEx.restype = c_int


def ToUn(vk, sc, kst, hkid):
    b = create_unicode_buffer(256)
    _ToUnicodeEx(vk, sc, kst, b, 256, 0, hkid)
    return b.value

def reallyUPPER(str):
    match = re.search(r"[!@#$%^&*()_+|}{:\"?><]",str)
    rtrn = False
    if match != None:
        rtrn = True
    if str.isupper():
        rtrn = True
    return rtrn
    
def Minuses(string):
    ids = []
    for id in string:
        ids.append(w3a.VkKeyScanEx(id,lcs.AllList()[0]))
    minpos = [id for id, x in enumerate(ids) if x == -1]
    return minpos
    
if __name__ == '__main__':
    inpt = input("Enter String:\n")
    inptloc = int(input("Enter layout id:\n"))
    minpos = Minuses(inpt)
    rst = ""
    print(minpos)
    for r in inpt:
        kst = create_string_buffer(256)
        if reallyUPPER(r):
            kst[16] = 0xff
        rst += ToUn(w3a.VkKeyScanEx(r,lcs.AllList()[0]),0,kst,inptloc)
    print(rst)