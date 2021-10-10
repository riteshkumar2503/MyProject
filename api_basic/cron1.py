#! /Users/apple/opt/anaconda3/envs/ritDjangoEnv/bin/python3.6
from django_cron import CronJobBase, Schedule
from datetime import datetime
from tasks_123 import celery_task1, celery_task2, celery_task3, celery_task_fullflow


class MyCronJob1(CronJobBase):
    RUN_EVERY_MINS = 1 # every 1 min
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'api_basic.my_cron_job111' # a unique code
    def do(self):
        print("helloooooo")
        print("current date and time 111111>>>>", datetime.now())


class MyCronJob2(CronJobBase):
    RUN_EVERY_MINS = 1 # every 1 min
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_cron_job222' # a unique code
    def do(self):
        print("byeeeeeee")
        print("current date and time 2222222>>>>", datetime.now())


class MyCronJob3(CronJobBase):
    RUN_AT_TIMES = ['13:50', '13:53', '13:56']  # ****** is in GMT
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'my_cron_job333'  # a unique code
    def do(self):
        print("iiiiiiiiiiiiiiiiiiiiiiiiiiii", datetime.now())


class MyCronJob4(CronJobBase):
    RUN_AT_TIMES = ['11:40']  # ****** is in GMT
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'my_cron_job444'  # a unique code
    def do(self):
        celery_task_fullflow.delay()
