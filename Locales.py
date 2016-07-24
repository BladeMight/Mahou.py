#!/usr/bin/env python3
import win32api as w3a, win32gui as w3g, win32process as w3p

def GetCurrentLocale():
    return w3a.GetKeyboardLayout(w3p.GetWindowThreadProcessId(w3g.GetForegroundWindow())[0]) & 0xFFFF
def AllList():
    locs = []
    for var in w3a.GetKeyboardLayoutList():
        locs.append(var & 0xFFFF)
    return locs;
def GetNotCurrentLocale():
    print(GetCurrentLocale())
    for o in AllList():
        if o != GetCurrentLocale():
            return o
def main():
    print("Runned as program.")
    print("Current locale is {}".format(GetCurrentLocale()))
    print("All locales:\n{}".format(AllList()))
if __name__ == '__main__':
    main()