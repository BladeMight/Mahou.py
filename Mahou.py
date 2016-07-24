#!/usr/bin/env python3
__version__ = '0.67-beta'
__author__ = 'BladeMight'
import win32gui as w3g, win32api as w3a, ctypes, atexit
import win32clipboard as w3cl
from KInputs import *
from win32con import *
from collections import namedtuple
from ctypes import wintypes, windll, CFUNCTYPE, POINTER, c_int, c_void_p
from time import sleep
import Locales as lcs
from ToUn import *
# Hotkeys & functions related to it
brf = ctypes.byref
u32 = ctypes.windll.user32
m = wintypes.MSG()
def HKHandle(ID):
    global self
    print("HK with id = {} fired.".format(ID))
    if ID == 0:
        '''Converts selection'''
        # Below needed for AllList to return correct next locale id.
        w3a.PostMessage(w3g.GetForegroundWindow(),0x50, lcs.GetNotCurrentLocale())
        ConvertSelection()
        print(self)
    if ID == 1 and not self:
        '''Converts typed last word'''
        ConvertLast(c_word)
    if ID == 65536:
        print("65536 = exit.\nExitting...")
        exit()
def RegHK(key, mods, ID):
    u32.RegisterHotKey(None, ID, mods, key)
def UnRegHK(ID):
    u32.UnregisterHotKey(None, ID)
def WndProc():
    while u32.GetMessageA(brf(m),None,0,0) != 0:
        if m.message == WM_HOTKEY:
            Key = (m.lParam >> 16) & 0xFFFF
            Modifs = m.lParam & 0xFFFF
            print("Key = {}, mods is {}.".format(Key,Modifs))
            HKHandle(m.wParam)
# KeyboardHook & related functions
KeyboardEvent = namedtuple('KeyboardEvent', ['event_type', 'key_code','scan_code', 'alt_pressed','time'])
c_word = []
self = False
shift = False
other = False
def listen():
    def low_level_handler(nCode, wParam, lParam):
        global c_word
        global shift
        global other
        Key = lParam[0] & 0xffff
        if Key == 160 or Key == 161 or Key == 16:
            shift = True if wParam == WM_KEYDOWN else False
        if Key == 91 or Key == 92 or \
             Key == 162 or Key == 163 or \
             Key == 163 or Key == 164 or Key == 18:
            other = True if wParam == WM_KEYDOWN else False
        if wParam == WM_KEYDOWN:
            if(34 <= Key <= 40 or
                           44 <= Key <= 46 or
                Key == 145 or Key == 19 or
                Key == 13 or Key == 32) \
                and not self:
                print("c_word Cleared!")
                c_word.clear()
            if Key == 8 and not self:
                if len(c_word) > 0:
                    del c_word[-1]
                    print("removed 1 item from c_word,\nnow lenght is {}".format(len(c_word)))
                else:
                    print("c_word is empty.")
            if(65 <= Key <= 90 or
                48 <= Key <= 57 or
                186 <= Key <= 192 or
                219 <= Key <= 222) \
               and not other and not self:
                kst = create_string_buffer(256)
                if not shift:
                    print(ToUn(Key,0,kst,lcs.GetCurrentLocale()))
                    c_word.append(YuKey(Key,False))
                else:
                    kst[16] = 0xff
                    print(ToUn(Key,0,kst,lcs.GetCurrentLocale()))
                    c_word.append(YuKey(Key,True))
        return windll.user32.CallNextHookEx(hook_id, nCode, wParam, lParam)
    CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
    pointer = CMPFUNC(low_level_handler)
    hook_id = windll.user32.SetWindowsHookExA(WH_KEYBOARD_LL, pointer, w3a.GetModuleHandle(None), 0)

    def low_level_mouse_handler(nCode, wParam, lParam):
        if wParam == WM_LBUTTONUP or wParam == WM_RBUTTONUP:
            print('c_word Cleared!')
            c_word.clear()
        return windll.user32.CallNextHookEx(hook2_id, nCode, wParam, lParam)
    pointer2 = CMPFUNC(low_level_mouse_handler)
    hook2_id = windll.user32.SetWindowsHookExA(WH_MOUSE_LL, pointer2,
                                             w3a.GetModuleHandle(None), 0)
    atexit.register(windll.user32.UnhookWindowsHookEx, hook_id)

    while True:
        try:
            msg = w3g.GetMessage(None, 0, 0)
            w3g.TranslateMessage(brf(msg))
            w3g.DispatchMessage(brf(msg))
        except TypeError:
            HKHandle(msg[1][2])
class YuKey(object):
    def __init__(self,VKCode,Upper):
        self.VKCode=VKCode
        self.Upper=Upper
def ConvertLast(c_word):
    '''Converts last inputted text'''
    w3a.PostMessage(w3g.GetForegroundWindow(), 0x50, lcs.GetNotCurrentLocale())
    global self
    self = True
    for x in range(len(c_word)):
        MakeInput(True,False,VK_BACK)
    for x in range(len(c_word)):
        print(str(c_word[x].VKCode) + '/' + str(c_word[x].Upper))
        if c_word[x].Upper:
            MakeInput(False,True,c_word[x].VKCode)
        else:
            MakeInput(False,False,c_word[x].VKCode)
    self = False
def ConvertSelection():
    '''Converts selected text'''
    global self
    self = True
    MakeInput(True,False,VK_RCONTROL,VK_INSERT)
    sleep(0.05)
    w3cl.OpenClipboard()
    data = w3cl.GetClipboardData()
    data.replace('\r\n','\n')
    w3cl.EmptyClipboard()
    w3cl.CloseClipboard()
    idslist = []
    for d in data:
        id = VkKeyScanEx(d, lcs.AllList()[0])
        idslist.append(id)
    print(idslist)
    minuses = Minuses(data)
    for l in lcs.AllList():
        for m1 in minuses:
            tr = VkKeyScanEx(data[m1],l)
            if tr != -1:
               idslist[m1] = tr
    if -1 in idslist:
        windll.user32.MessageBoxW(None,'Selection contains unrencongnized characters.','What?',0)
    else:
        print(idslist)
        for count,id in enumerate(idslist):
            if reallyUPPER(data[count]):
                MakeInput(False,True,id)
            else:
                MakeInput(False,False,id)
        for _ in range(len(data)):
            MakeInput(True,True,VK_LEFT)
    self = False
def main():
    print('Mahou.py ' +__version__ + ' by ' + __author__ + ' started.')
    RegHK(VK_F4, MOD_ALT + MOD_SHIFT, 65536)
    RegHK(VK_F7, 0,                   0)
    RegHK(VK_F6, 0,                   1)
    listen()
    print('Global exit hotkey is ALT+SHIFT+F4, F7 to convert selection, F6 to convert last word.')
    WndProc()
if __name__ == '__main__':
    main()