import tkinter as tk
import json
import os
from tkinter.constants import TRUE
from operator import itemgetter

DEFAULT_BED_TIME = (0, 0)
BEDTIME_DATA = './bedtime.json'


def getBedtime():
    if not os.path.exists(BEDTIME_DATA):
        return DEFAULT_BED_TIME

    with open(BEDTIME_DATA) as dataFile:
        data = json.load(dataFile)
        print(data)
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


DEFAULT_CONFIG = {
    "font": ('Arial', 50),


}

DEFAULT_INPUT_CONFIG = {
    **DEFAULT_CONFIG,
}


DEFAULT_HOUR_INPUT_CONFIG = {
    ** DEFAULT_INPUT_CONFIG,
    **{"width": 2, },
}


DEFAULT_MINUTE_INPUT_CONFIG = {
    ** DEFAULT_INPUT_CONFIG,
    **{"width": 2, },
}


class ValidatedNumberInput(tk.Frame):
    def __init__(self, root, value, min, max, handleChange, config=DEFAULT_MINUTE_INPUT_CONFIG):
        super().__init__(root)
        self._root = root
        self._value = value
        self._min = min
        self._max = max
        self._handleChange = handleChange
        self._config = {**DEFAULT_MINUTE_INPUT_CONFIG, **config}
        self._createContent()

    def _updateValue(self, *args):
        stringVal = self.stringVar.get()
        self._handleChange(stringVal)

    def _validateInput(self, valueStr, reason):
        if(reason == 'key'):
            if(valueStr == ''):
                return True

            try:
                value = int(valueStr)
                if(value < self._min or value > self._max):
                    raise Exception("number is not within specific bounds")
                return True
            except Exception:
                return False

        return True

    def _createContent(self):

        font, width = itemgetter('font', 'width')(self._config)
        stringVar = tk.StringVar()
        stringVar.set(str(self._value))
        self.stringVar = stringVar

        stringVar.trace("w", self._updateValue)

        regIsValidInput = self._root.register(self._validateInput)
        self.entry = tk.Entry(self, validate="all",
                              validatecommand=(regIsValidInput, '%P', '%V'), font=font, width=width, textvariable=stringVar)

        self.entry.pack(side=tk.BOTTOM)


class PaddedValidatedNumberInput(tk.Frame):
    def __init__(self, root, value, min, max, handleChange, numChars, config=DEFAULT_MINUTE_INPUT_CONFIG):
        super().__init__(root)
        self._validatedNumberInputParams = dict(value=value,
                                                min=min, max=max, handleChange=handleChange, config=config)
        self._numChars = numChars
        self._config = {**DEFAULT_MINUTE_INPUT_CONFIG, **config}
        self._createContent()

    def _handleFocusout(self, *args):
        print('handle focus out')
        stringVal = self._validatedNumberInput.stringVar.get()
        stringValLen = len(stringVal)
        if stringValLen > 0 and stringValLen < self._numChars:
            numPad = self._numChars - len(stringVal)
            padded = '0'*numPad+stringVal
            self._validatedNumberInput.stringVar.set(padded)

    def _createContent(self):
        self._validatedNumberInput = ValidatedNumberInput(
            self, **self._validatedNumberInputParams)
        self._validatedNumberInput.entry.bind(
            '<FocusOut>', self._handleFocusout)
        self._validatedNumberInput.pack()


class HourInput(tk.Frame):
    def __init__(self, root, hour, handleChange, config=DEFAULT_HOUR_INPUT_CONFIG):
        super().__init__(root)
        self._config = {**DEFAULT_HOUR_INPUT_CONFIG, **config}
        self._paddedValidatedNumberInputParams = dict(
            value=hour, min=0, max=23, handleChange=handleChange, numChars=2, config=self._config)
        self._root = root
        self._createContent()

    def _createContent(self):
        self._paddedValidatedNumberInput = PaddedValidatedNumberInput(
            self, **self._paddedValidatedNumberInputParams)
        self._paddedValidatedNumberInput.pack()


class MinuteInput(tk.Frame):
    def __init__(self, root, minute, handleChange, config=DEFAULT_MINUTE_INPUT_CONFIG):
        super().__init__(root)
        self._paddedValidatedNumberInputParams = dict(
            value=minute, min=0, max=59, handleChange=handleChange, numChars=2, config=config)
        self._root = root
        self._createContent()

    def _createContent(self):
        self._paddedValidatedNumberInput = PaddedValidatedNumberInput(
            self, **self._paddedValidatedNumberInputParams)
        self._paddedValidatedNumberInput.pack()


class TimeInput(tk.Frame):
    def __init__(self, root, hour, minute, handleChange, config=DEFAULT_CONFIG):
        super().__init__(root)
        self._root = root
        self._handleChange = handleChange
        self._config = {**DEFAULT_CONFIG, **config}
        self._hour = hour
        self._minute = minute
        self._createContent()
        self._runChangeHandler()

    def _setHour(self, hour):
        self._hour = hour
        self._runChangeHandler()

    def _setMinute(self, minute):
        self._minute = minute
        self._runChangeHandler()

    def _runChangeHandler(self):
        self._handleChange(self._hour, self._minute)

    def _createContent(self):
        hourInput = HourInput(self, hour=self._hour, handleChange=self._setHour,
                              config=self._config)
        hourInput.pack(side=tk.LEFT)

        font = itemgetter('font')(self._config)
        colon = tk.Label(self, text=':', font=font)
        colon.pack(side=tk.LEFT)

        minuteInput = MinuteInput(
            self, minute=self._minute, handleChange=self._setMinute, config=self._config)
        minuteInput.pack(side=tk.LEFT)


class SubmitButton(tk.Frame):
    def __init__(self, root, handleClick, config=DEFAULT_CONFIG):
        super().__init__(root)
        self._root = root
        self._handleClick = handleClick
        self._config = {**DEFAULT_CONFIG, **config}
        self._createContent()

    def _createContent(self):
        font = itemgetter('font')(self._config)
        self._button = tk.Button(
            self, text="Set", font=font, command=self._handleClick)
        self._button.pack()

    def enable(self):
        self._button['state'] = tk.NORMAL

    def disable(self):
        self._button['state'] = tk.DISABLED


class TimeForm(tk.Frame):
    def __init__(self, root, hour, minute, handleChange):
        super().__init__(root)

        self._root = root
        self._hour = hour
        self._minute = minute
        self._submitButton = None
        self._handleChange = handleChange
        self._createContent()
        self._updateSubmitState()

    def _onTimeChange(self, hourStr, minuteStr):
        self._hour = None if hourStr == '' else getHour(hourStr)
        self._minute = None if minuteStr == '' else getMinute(minuteStr)
        self._updateSubmitState()

    def _updateSubmitState(self):
        valdated = self._hour != None and self._minute != None
        if self._submitButton:
            if valdated:
                self._submitButton.enable()
            else:
                self._submitButton.disable()

    def _setTime(self):
        self._handleChange(self._hour, self._minute)

    def _createContent(self):
        timeInput = TimeInput(
            self, hour=self._hour, minute=self._minute, handleChange=self._onTimeChange)
        timeInput.pack(side=tk.LEFT)
        self._submitButton = SubmitButton(self, handleClick=self._setTime)
        self._submitButton.pack(side=tk.RIGHT)
        self._updateSubmitState()


class MainWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self._getBedtime()

        self._root = root
        self._configureTopLevel()
        self._createContent()

    def _getBedtime(self):
        (bedtimeHours, bedtimeMinutes) = getBedtime()
        self._bedtimeHours = bedtimeHours
        self._bedtimeMinutes = bedtimeMinutes

    def _configureTopLevel(self):
        self._root.geometry("500x500+500+100")
        self._root.update_idletasks()
        self._root.overrideredirect(True)

    def _createContent(self):
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self._addMessage()
        self._addTimeInput()

    def _addMessage(self):
        message = 'BEDTIME'
        message = tk.Label(self, text=message, font=('Arial', 50))
        message.pack(side=tk.TOP)

    def _updateBedtime(self, hours, minutes):
        setBedtime(hours, minutes)

    def _addTimeInput(self):
        timeForm = TimeForm(self, self._bedtimeHours,
                            self._bedtimeMinutes, handleChange=self._updateBedtime)
        timeForm.pack(side=tk.BOTTOM)
