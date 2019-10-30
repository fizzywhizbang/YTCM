#!/usr/bin/env python3
import threading
import os
from apscheduler.schedulers.blocking import BlockingScheduler
import monitor
import subprocess
from libs.cmds import MyPrompt

def channels_update():
    command = "./ytcm.py -u -d"

    subprocess.Popen(command.split(), shell=False)

def run():
    channels_update()
    scheduler = BlockingScheduler()
    scheduler.add_job(channels_update, 'interval', hours=1)
    scheduler.start()


 
if __name__ == '__main__':
    t1 = threading.Thread(target=run)
    t1.start()

    MyPrompt().cmdloop()
    
