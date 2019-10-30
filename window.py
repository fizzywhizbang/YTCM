import commander
from commander import Command
from commander import Commander
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
    
        def do_add(self, inp):
            name = input("Please give channel name: ")
            dldir = input("Please give download dir: ")
            http = input("Please give the channel URL: ")
            proc = subprocess.Popen(["./ytcm.py", "-a", name , dldir, http], stdout=subprocess.PIPE)
            out = proc.stdout.read()
            c.output(out, 'green')
            # add_string = "./ytcm.py -a \"" + name + "\" \"" + dldir + "\" "  + http
            # os.system(add_string)
            # print("adding %s" % add_string)

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
        
        def do_list(self):
            # channel_list = get_chan_list()
            proc = subprocess.Popen(["./ytcm.py", "-c"], stdout=subprocess.PIPE)
            out = proc.stdout.read()
            c.output(out, 'green')
            # os.system('./ytcm.py -c')

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