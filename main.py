#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  unbenannt.py
#  
#  Copyright 2013 Heinrich Speich <tiger@radon>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys, os
from datetime import datetime, timedelta
import time
import random
import sys
import pynotify
import pygst
import gst
from mylogging import Logger

# even in Python this is globally nasty, do something nicer in your own code
capabilities = {'actions':     False,
        'body':                False,
        'body-hyperlinks':     False,
        'body-images':         False,
        'body-markup':         False,
        'icon-multi':          False,
        'icon-static':         False,
        'sound':               False,
        'image/svg+xml':       False,
        'private-synchronous': False,
        'append':              False,
        'private-icon-only':   False}
        
class Player:
    def __init__(self):
        self.player = gst.element_factory_make("playbin2", "player")
        self.fakesink = gst.element_factory_make("fakesink", "fakesink")
        self.player.set_property("video-sink", self.fakesink)
        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message", self.on_message)
        
    def on_message(self, bus, message):
        t = message.type
        #print message
        #print t
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            #print "End of file"
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            #print "Error: %s" % err, debug
        
    def play(self, filepath):
        #print "Spiele " + filepath
        self.player.set_state(gst.STATE_NULL)
        if os.path.isfile(filepath):
            fullname = os.path.abspath(filepath)
            self.player.set_property("uri", "file://" + fullname)
            self.player.set_state(gst.STATE_PLAYING)

def initCaps ():
    caps = pynotify.get_server_caps()
    if caps is None:
        #print "Failed to receive server caps."
        sys.exit(1)
 
    for cap in caps:
        capabilities[cap] = True
        
        
def play_random_voice(pl, voices, logger):
    num = random.randrange(0,len(voices),1)
    pl.play(voices[num])
    birdname = get_bird_name(voices[num])
    logger.write_info("Es singt der/die " + birdname)
    print_note(birdname)
    return 0

def print_note(text):
    n = pynotify.Notification("Vogelstimme", text, "notification-message-im")
    n.show()
    
def get_bird_name(filename):
    answ = filename.replace(".mp3","")
    junk, sep, answ = answ.partition(" - ")
    
    return answ
    
    
def main():
    pl = Player()
    logger = Logger(os.environ['HOME'] + "/birdclock.log")
    logger.write_info("Programm gestartet")
    
    if not pynotify.init ("icon-summary-body"):
        logger.write_error("Initialisierung pynotify ist fehlgesclagen")
        sys.exit (1)
 
    # call this so we can savely use capabilities dictionary later
    initCaps ()
    
    #print_note("I started")
      
    #The Clock - play a bird every hour
    dt = datetime.now()
    voices = []
    startpath = os.path.dirname(__file__)
    logger.write_info("Suchpfad für die Stimmendateien: " + startpath)
    for dirpath, dirnames, filenames in os.walk(startpath):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if f.endswith(".mp3"):
                voices.append(fp)
            
    #print voices
    #play_random_voice(pl, voices)
    while True:
        dt = datetime.now()
        nexthourDt = dt.replace(minute=0, second=0)
        nexthourDt += timedelta(hours=1)
        logger.write_info("Nächste Stimme um {0}".format(nexthourDt))
        while datetime.now() < nexthourDt:
            time.sleep(10)
            
        play_random_voice(pl, voices, logger)
        
    return 0


if __name__ == '__main__':
    main()

