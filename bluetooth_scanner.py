#!/usr/bin/env python
# program runs in the background, scanning for bluetooth devices 
# at a regular interval. 
# This code is meant to be run in Linux, not in OS or Windows
# For installation pygame in Linux, open a terminal and run sudo apt-get install python-pygame

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

AWAY_HEURISTIC = 10

pygame.mixer.init()



def get_bt_ids():
    #"""Get all nearby IDs"""
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
            
            if pygame.mixer.get_init():

                audio_record = pygame.mixer.Sound("02.wav")
                audio_player = audio_record.play(maxtime=2000) #play the sound for two seconds

            else:
                print "pygame mixer is not initialized"
        else:

            pass
    # print ids  # it will print ["Linhao's", "Linhao's"]
    return ids



def scan():
    """Scan the area for bluetooth devices. If a new device is seen, notify the database."""
    # note the current time
    time = datetime.now()
    # get all of the bluetooth devices nearby
    ids = get_bt_ids()
    for id in ids:
        print id + " is coming\n"


def cleanup():
    """Clean up the list of nearby devices"""
    # keys to delete
    del_keys = []
    # get the current time
    time = datetime.now()
    # if any of the devices are stale, remove them from the list
    for device in devices_here:
        # get the last time the device was seen
        last_seen = devices_here[device]
        # if this device was last seen too long ago
        if (time - last_seen).seconds > AWAY_HEURISTIC:
            # flag it for removal to avoid
            # RuntimeError: dictionary changed size during iteration
            del_keys.append(device)
            # and notify the server that the device left
            upload_to_db({'time': time, 'device_id': device, 
                          'scanner_id': scanner_id, 'event_type': 'EXIT'})

    # remove flagged ids from the list of devices
    for k in del_keys:
        del devices_here[k]

def upload_to_db(params):
    """Upload data about an event to the server"""
    print '%s: device %s at time %s' % (params['event_type'], params['device_id'], params['time'])
    # massage the params to be right
    params['time'] = params['time'].strftime('%Y-%m-%d %H:%M:%S')
    # encode some parameters
    data = urlencode(params.items())
    try: 
        # post data to http://dev.hci.uma.pt/~boris/visits.php
        # going by IP is faster than doing a DNS lookup
        urlopen('http://dev.hci.uma.pt/~boris/visits.php', data)
    except URLError:
        print "...failed to upload data for event"
    
if __name__ == '__main__':
    while True:
        print "..."
        # continuously scan the world for new devices 
        scan()
        # and clean up the list of devices that are present
        # cleanup()

    
