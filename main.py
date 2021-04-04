import tkinter as tk
from apscheduler.schedulers.background import BackgroundScheduler
from utils import getBedtime
from bedtime_manager import BedtimeManager


(hour, minute) = getBedtime()
root = tk.Tk()
scheduler = BackgroundScheduler(daemon=True)
BedtimeManager(root, scheduler, hour, minute)
scheduler.start()
root.mainloop()
scheduler.shutdown()
