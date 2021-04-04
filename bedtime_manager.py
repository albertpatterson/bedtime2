import tkinter as tk
from main_window import MainWindow
from fullscreen_window import FullscreenWindow
from snooze import snooze


class BedtimeManager:
    def __init__(self, root,  scheduler, hour, minute):
        self._root = root
        self._scheduler = scheduler
        self._hour = hour
        self._minute = minute
        self._sleeping = False
        self._cancelStopSleepingJob = None
        self._setBedtimeSchedule()
        self._createContent()

    def _setBedtimeSchedule(self):
        self._isBedtimeJob = self._scheduler.add_job(
            self._startSleeping, 'cron', hour=self._hour, minute=self._minute)

    def _startSleeping(self):
        if self._cancelStopSleepingJob != None:
            self._cancelStopSleepingJob()
            self._cancelStopSleepingJob = None

        self._sleeping = True
        self._cancelStopSleepingJob = snooze(
            4*60*60*1e3, self._showFullscreenWindow, self._stopSleeping)

    def _stopSleeping(self):
        if self._cancelStopSleepingJob != None:
            self._cancelStopSleepingJob()
            self._cancelStopSleepingJob = None
        self._sleeping = False
        self._hideFullscreenWindow()

    def _showFullscreenWindow(self):
        self._fullscreenWindow.show()
        self._root.after(0, self._fullscreenWindow.show())

    def _hideFullscreenWindow(self):
        self._fullscreenWindow.hide()
        self._root.after(0, self._fullscreenWindow.hide())

    def _rescheduleBedtime(self, hour, minute):
        self._isBedtimeJob.reschedule('cron', hour=hour, minute=minute)
        self._stopSleeping()

    def _unSnooze(self):
        if(self._sleeping):
            self._showFullscreenWindow()
        else:
            self._hideFullscreenWindow()

    def _handleSnooze(self):
        snooze(5*60, self._hideFullscreenWindow, self._unSnooze)

    def _createContent(self):
        MainWindow(self._root, handleChange=self._rescheduleBedtime)
        fullScreenTopLevel = tk.Toplevel(self._root)
        self._fullscreenWindow = FullscreenWindow(
            fullScreenTopLevel, handleSnooze=self._handleSnooze)
