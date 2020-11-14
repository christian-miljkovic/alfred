import os
import sys
import logging
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from . import tasks


@sched.scheduled_job(
    CronTrigger.from_crontab("*/5 * * * *"), id="send_birthday_reminders", name="send_birthday_reminders"
)
def send_birthday_reminders():
    pass