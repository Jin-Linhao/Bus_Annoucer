#!/usr/bin/env python
# program runs in the background, scanning for bluetooth devices 
# at a regular interval. 
# This code is meant to be run in Linux, not in OS or Windows
# For installation pygame in Linux, open a terminal and run sudo apt-get install python-pygame
# For iPad bluetooth, the discover range is less than 15m.

__author__ = 'JIN Linhao'
__date__ = '07/Mar/2016'
__contact__ = 'jin_linhao@hotmail.com'


import os, time, platform
from datetime import datetime
from urllib import urlencode
from urllib2 import urlopen, URLError
import pygame.mixer
from pygame.locals import *
# get the name of this scanner
scanner_id = os.popen('uname -n').readline().strip()


dic = {"Linhao's":["02.wav", "Bus179"], 
       "jitete's":["03.wav", "Bus199"]}




def get_bt_ids():
    """Get all nearby IDs"""
    ids = []

    # launch the scanner
    f = os.popen('hcitool scan --length=2')
    # get the output from the scanner utility
    unparsed_data = f.readlines()[:]

    for u in unparsed_data:
        # get the ID of the bluetooth devices
        test = u.split()[:]
        # print test
        id = u.split()[1]
        if id == "jitete's":
            ids.append(id)
        elif id == "Linhao's":
            ids.append(id)

        else:
            pass


    return ids



def scan():
    """Scan the area for bluetooth devices. If a new device is seen, notify the database."""
    # note the current time
    time = datetime.now()
    # get all of the bluetooth devices nearby
    ids = get_bt_ids()
    for id in ids:
        if pygame.mixer.get_init():
            audio_record = pygame.mixer.Sound("audio/"+dic[id][0])
            audio_player = audio_record.play(maxtime=2000) #play the sound for two seconds
            print dic[id][1]
        



if __name__ == '__main__':

    pygame.mixer.init()

    while True:
        print "..."
        # continuously scan the world for new devices 
        scan()

    
