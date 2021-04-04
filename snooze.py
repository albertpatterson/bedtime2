from apscheduler.schedulers.background import BackgroundScheduler


def snooze(time, onSnooze, onUnsnooze):

    unSnoozeJob = None
    sched = BackgroundScheduler(daemon=True)

    def clearJob():
        nonlocal unSnoozeJob

        if unSnoozeJob == None:
            return

        unSnoozeJob.remove()
        unSnoozeJob = None

    def unSnooze():
        clearJob()
        onUnsnooze()

    unSnoozeJob = sched.add_job(
        unSnooze, 'interval', seconds=time)
    sched.start()

    onSnooze()

    return clearJob
