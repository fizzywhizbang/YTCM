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
from apscheduler.schedulers.blocking import BlockingScheduler
import os


def get_chan_list() -> str:
    proc = subprocess.Popen(["./ytcm.py", "-c"], stdout=subprocess.PIPE)
    out = proc.stdout.read()
    return out
    # os.system('./ytcm.py -c')



if __name__=='__main__':
    class TestCmd(Command):
        def do_exit(self, inp):
            print("Bye")
            return True
    
        def help_exit(self):
            print('exit the application. Shorthand: x q Ctrl-D.')
    
        def do_add(self, name, dldir, http):
            '''To add a new channel type: add 'name of the channel' 'download directory' https://youtube.com/channel/xxxxxx\n where the x's are the channel id or name'''
            proc = subprocess.Popen(["./ytcm.py", "-a", name , dldir, http], stdout=subprocess.PIPE)
            out = proc.stdout.read()
            c.output(out, 'green')
            # add_string = "./ytcm.py -a \"" + name + "\" \"" + dldir + "\" "  + http
            # os.system(add_string)
            # print("adding %s" % add_string)

      
        def do_update(self):
            '''This will update all channel videos'''
            proc = subprocess.Popen(["./ytcm.py", "-u"], stdout=subprocess.PIPE)
            out = proc.stdout.read()
            c.output(out, 'green')
       
        def do_mark(self):
            '''This will mark all videos downloaded.'''
            proc = subprocess.Popen(["./ytcm.py", "-m"], stdout=subprocess.PIPE)
            out = proc.stdout.read()
            c.output(out, 'green')

      
        def do_download(self, inp):
            '''This will download all videos in the queue.'''
            proc = subprocess.Popen(["./ytcm.py", "-d"], stdout=subprocess.PIPE)
            out = proc.stdout.read()
            c.output(out, 'green')
        
        def do_list(self):
            '''This will list all channels you are monitoring'''
            channel_list = get_chan_list()
            c.output(channel_list, 'green')
            
        def default(self, inp):
            if inp == 'x' or inp == 'q':
                return self.do_exit(inp)

        def do_raise(self, *args):
            raise Exception('Some Error')
        
    c=Commander('Youtube Channel Monitor', cmd_cb=TestCmd())
    
    #Test asynch output -  e.g. comming from different thread
    import time
    def channels_update():
        # os.system('./ytcm.py -u -d')
        c.output("starting update:", "magenta")
        proc = subprocess.Popen(["./ytcm.py", "-u", "-d"], stdout=subprocess.PIPE)
        while True:
            nextline = proc.stdout.readline()
            if len(nextline) >=1:
                c.output(nextline, 'magenta')
            
                

    def run():
        c.output("Monitoring Channels For Updates", "green")
        channels_update()
        scheduler = BlockingScheduler()
        scheduler.add_job(channels_update(), 'interval', hours=1)
        scheduler.start()


    t=Thread(target=run)
    t.daemon=True
    t.start()
    
    #start main loop
    c.loop()