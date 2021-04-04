import os
import json
from constants import *


def getBedtime():
    if not os.path.exists(BEDTIME_DATA):
        return DEFAULT_BED_TIME

    with open(BEDTIME_DATA) as dataFile:
        data = json.load(dataFile)
        bedtimeHours = data["bedtimeHours"]
        bedtimeMinutes = data["bedtimeMinutes"]

        validBedtime = not (bedtimeHours == None or bedtimeMinutes == None)
        return (bedtimeHours, bedtimeMinutes) if validBedtime else DEFAULT_BED_TIME


def setBedtime(bedtimeHours, bedtimeMinutes):
    data = {"bedtimeHours": bedtimeHours, "bedtimeMinutes": bedtimeMinutes}
    with open(BEDTIME_DATA, 'w+') as dataFile:
        json.dump(data, dataFile)


def getHour(hourStr):
    hour = int(hourStr)
    if(hour < 0 or hour > 23):
        raise Exception("number is not a valid hour")

    return hour


def getMinute(minuteStr):
    minute = int(minuteStr)
    if(minute < 0 or minute > 59):
        raise Exception("number is not a valid minute")

    return minute
