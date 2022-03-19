from apscheduler.schedulers.blocking import BlockingScheduler
import os

sched = BlockingScheduler()

# Modify the cron schedule to your own intent 
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=2)
def timed_job():
    # Change the command below to modify the arguments of the script
    # The arguments answer to the input required by the script
    os.system('python main.py #options')


sched.start()