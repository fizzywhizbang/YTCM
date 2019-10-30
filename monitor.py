#!/usr/bin/env python3
from apscheduler.schedulers.blocking import BlockingScheduler
import os


def channels_update():
    os.system('./ytcm.py -u -d')



def run():
    channels_update
    scheduler = BlockingScheduler()
    scheduler.add_job(channels_update, 'interval', hours=1)
    scheduler.start()