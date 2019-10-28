#!/usr/bin/env python3
from apscheduler.schedulers.blocking import BlockingScheduler
import os

def channels_update():
    os.system('./ytcm.py -u -jd') #run monitor


os.system('./ytcm.py -u -jd') #run initial start script
scheduler = BlockingScheduler()
scheduler.add_job(channels_update, 'interval', hours=1)
scheduler.start()