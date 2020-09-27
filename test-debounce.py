# -*- coding: utf-8 -*-

"""
Created on 13 Nov 2014
Used to test any bounce of keyboard switches

Can change the BOUNCE_TIME with a lower value than the automatic repeat key system
Mine on ubuntu is 40ms after a 660ms pause (display with this python script ..),
Actual mechanics switch has value like 5-10ms debounce time
"""

__author__ = 'hacketo'

import termios, fcntl, sys, os
import time

keys = {}

BOUNCE_TIME = 30
"""
Change this value to anything lower than the automatic repeat key system
"""

def loopKeys():
    """
    Check if the time between two same key taped is lower than the BOUNCE_TIME const value,
    then print some informations about the bounce time
    """
    global keys

    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    try:
        while 1:
            try:
                c = sys.stdin.read(1)
                t = getCurrentMillisec()
                if c in keys:
                    timePassed = t - keys[c]
                    if timePassed <= BOUNCE_TIME:
                        print "bounce : %s , %d"%(c, timePassed)
                keys[c] = t
            except IOError: pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)


def getCurrentMillisec():
    return int(round(time.time() * 1000))


if __name__ == "__main__":
    loopKeys()
