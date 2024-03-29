#!/usr/bin/env python3
# YTCM - Youtube Channel Monitor
# Copyright (C) 2019  Marc Levine
#
# This file is part of YTCM.
#
# YTCM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# YTCM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with YTCM.  If not, see <http://www.gnu.org/licenses/>.
import libs.commander
from libs.commander import Command
from libs.commander import Commander
from threading import Thread
import threading
import subprocess
import os
from time import sleep
import datetime

def get_chan_list() -> str:
    proc = subprocess.Popen(["./ytcm.py", "-c"], stdout=subprocess.PIPE)
    out = proc.stdout.read()
    return out
    # os.system('./ytcm.py -c')

def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__=='__main__':
    class TestCmd(Command):
        def do_exit(self, inp):
            print("Bye")
            return True
    
        def help_exit(self):
            print('exit the application. Shorthand: x q Ctrl-D.')
    
        def do_add(self,name,dldir,http):
            '''To add a new channel type: add name of the channel,download directory,https://youtube.com/channel/xxxxxx\n where the x's are the channel id or name'''
            
            proc = subprocess.Popen(["./ytcm.py", "-a", name , dldir, http], stdout=subprocess.PIPE)
            out = proc.stdout.read()
            c.output(out, 'green')
            proc = subprocess.Popen(["./ytcm.py", "-u"], stdout=subprocess.PIPE)
            self.do_listvideos("null")

        def do_get_all(self,inp):
            '''Use this to rip all videos from a channel. Be careful it could be slooooow'''
            

        def do_update(self,inp):
            '''This will update all channel videos'''
            proc = subprocess.Popen(["./ytcm.py", "-u"], stdout=subprocess.PIPE)
            out = proc.stdout.read()
            c.output(out, 'green')
            self.do_list
       
        def do_mark(self,inp):
            '''This will mark all videos downloaded.'''
            proc = subprocess.Popen(["./ytcm.py", "-m"], stdout=subprocess.PIPE)
            out = proc.stdout.read()
            c.output(out, 'green')

        def do_listvideos(self,inp):
            '''This will list all videos in the queue'''
            proc = subprocess.Popen(["./ytcm.py", "-l"], stdout=subprocess.PIPE)
            while True:
                nextline = proc.stdout.readline()
                if len(nextline) >=1:
                    c.output(nextline, 'green')
                else:
                    break

        def do_delete(self,chan):
            '''This is to delete a channel from your subscriptions delete \"channel name\"'''
            proc = subprocess.Popen(["./ytcm.py", "-r", chan], stdout=subprocess.PIPE)
            out = proc.stdout.read()
            c.output(out, 'magenta')            
      
        def do_download(self, inp):
            '''This will download all videos in the queue.'''
            proc = subprocess.Popen(["./ytcm.py", "-d"], stdout=subprocess.PIPE)
            out = proc.stdout.read()
            c.output(out, 'green')
        
        def do_list(self,inp):
            '''This will list all channels you are monitoring'''
            channel_list = get_chan_list()
            c.output(channel_list, 'green')
            
        def default(self, inp):
            if inp == 'x' or inp == 'q':
                return self.do_exit(inp)
            if inp == 'lv':
                return self.do_listvideos(inp)

        def do_raise(self, *args):
            raise Exception('Some Error')
        
    c=Commander('Youtube Channel Monitor', cmd_cb=TestCmd())
    
    #Test asynch output -  e.g. comming from different thread
    import time
    def channels_update():
        # os.system('./ytcm.py -u -d')
        c.output("starting update: {}".format(now()), "magenta")
        proc = subprocess.Popen(["./ytcm.py", "-u", "-d"], stdout=subprocess.PIPE)
        while True:
            nextline = proc.stdout.readline()
            if len(nextline) >=1:
                c.output(nextline, 'magenta')
            else:
                break
        c.output("update complete: {}".format(now()), "green")    
                

    def run():
        while True:
            c.output("Monitoring Channels For Updates", "green")
            channels_update()
            sleep(60*60) #wait one hour before looping so as not to get banned by YT


    t=Thread(target=run)
    t.daemon=True
    t.start()
    
    #start main loop
    c.loop()