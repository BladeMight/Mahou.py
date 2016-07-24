#!/usr/bin/env python3
from win32api import *
from win32con import *
from time import *
def MakeInput(extend,shift, *keys):
    ext = 1 if extend else 0
    if shift:
        keybd_event(VK_SHIFT,0,1,0)
    for key in keys:
        keybd_event(key,0,ext,0)
    sleep(0.005)
    for key in keys:
        keybd_event(key,0,ext | 2,0)
    keybd_event(VK_SHIFT,0,1 | 2,0)
if __name__ == "__main__":
    print("Demo of CTRL+SHIFT+ESC simulate.")
    MakeInput(True,True,VK_CONTROL,VK_ESCAPE)