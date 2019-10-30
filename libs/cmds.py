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

from cmd import Cmd
import os
import monitor
import subprocess

class MyPrompt(Cmd):
    prompt = 'ytcm> '
    intro = "Welcome! Type ? to list commands"
 
    def do_exit(self, inp):
        print("Bye")
        return True
    
    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')
 
    def do_add(self, inp):
        name = input("Please give channel name: ")
        dldir = input("Please give download dir: ")
        http = input("Please give the channel URL: ")
        add_string = "./ytcm.py -a \"" + name + "\" \"" + dldir + "\" "  + http
        os.system(add_string)
        print("adding %s" % add_string)

    def help_add(self):
        print("Add a new channel to the system.")
 
    def do_update(self, inp):
        os.system("./ytcm.py -u")
    def help_update(self):
        print("This will update all channel videos")
    def do_mark(self, inp):
        os.system("./ytcm.py -m")
    def help_mark(self):
        print("This will mark all videos downloaded.")
    def do_download(self, inp):
        os.system("./ytcm.py -d")

    def help_download(self):
        print("This will download all videos in the queue.")
    def do_list(self, inp):
        os.system('./ytcm.py -c')

    def do_monitor(self, inp):
        # run()
        print("monitor")

    def help_monitor(self):
        print("This will start the monitoring of all saved channels.")
    def help_list(self, inp):
        print("list all channels.")

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
        if inp == "m":
            self.do_mark(inp)
        if inp == "s":
            self.do_monitor(inp)
 
 
    do_EOF = do_exit
    help_EOF = help_exit