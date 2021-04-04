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

    def setValue(self, valueStr):
        if(self._validateInput(valueStr)):
            self.stringVar.set(valueStr)
            self._updateValue()

    def _updateValue(self, *args):
        stringVal = self.stringVar.get()
        self._handleChange(stringVal)

    def _validateOnlyKeyInput(self, valueStr, reason):
        if(reason == 'key'):
            return self._validateInput(valueStr)

        return True

    def _validateInput(self, valueStr):
        if(valueStr == ''):
            return True

        try:
            value = int(valueStr)
            if(value < self._min or value > self._max):
                raise Exception("number is not within specific bounds")
            return True
        except Exception:
            return False

    def _createContent(self):

        font, width = itemgetter('font', 'width')(self._config)
        stringVar = tk.StringVar()
        stringVar.set(str(self._value))
        self.stringVar = stringVar

        stringVar.trace("w", self._updateValue)

        regIsValidInput = self._root.register(self._validateOnlyKeyInput)
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

    def setValue(self, valueStr):
        self._validatedNumberInput.setValue(valueStr)

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

    def setValue(self, valueStr):
        self._paddedValidatedNumberInput.setValue(valueStr)

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

    def setValue(self, valueStr):
        self._paddedValidatedNumberInput.setValue(valueStr)

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

    def setTime(self, hourStr, minuteStr):
        self._hourInput.setValue(hourStr)
        self._minuteInput.setValue(minuteStr)

    def _setHour(self, hour):
        self._hour = hour
        self._runChangeHandler()

    def _setMinute(self, minute):
        self._minute = minute
        self._runChangeHandler()

    def _runChangeHandler(self):
        self._handleChange(self._hour, self._minute)

    def _createContent(self):
        self._hourInput = HourInput(self, hour=self._hour, handleChange=self._setHour,
                                    config=self._config)
        self._hourInput.pack(side=tk.LEFT)

        font = itemgetter('font')(self._config)
        colon = tk.Label(self, text=':', font=font)
        colon.pack(side=tk.LEFT)

        self._minuteInput = MinuteInput(
            self, minute=self._minute, handleChange=self._setMinute, config=self._config)
        self._minuteInput.pack(side=tk.LEFT)


class StatefulButton(tk.Frame):
    def __init__(self, root, label, handleClick, config=DEFAULT_CONFIG):
        super().__init__(root)
        self._root = root
        self._label = label
        self._handleClick = handleClick
        self._config = {**DEFAULT_CONFIG, **config}
        self._createContent()

    def _createContent(self):
        font = itemgetter('font')(self._config)
        self._button = tk.Button(
            self, text=self._label, font=font, command=self._handleClick)
        self._button.pack()

    def enable(self):
        self._button['state'] = tk.NORMAL

    def disable(self):
        self._button['state'] = tk.DISABLED


class TimeForm(tk.Frame):
    def __init__(self, root, hour, minute, handleChange):
        super().__init__(root)

        self._root = root
        self._hourPrev = hour
        self._minutePrev = minute
        self._hour = hour
        self._minute = minute
        self._submitButton = None
        self._handleChange = handleChange
        self._createContent()
        self._updateButtonState()

    def _onTimeChange(self, hourStr, minuteStr):
        self._hour = None if hourStr == '' else getHour(hourStr)
        self._minute = None if minuteStr == '' else getMinute(minuteStr)
        self._updateButtonState()

    def _updateButtonState(self):
        buttonsReady = self._submitButton and self._resetButton
        valdated = self._hour != None and self._minute != None
        changed = self._hour != self._hourPrev or self._minute != self._minutePrev
        if buttonsReady:
            if valdated and changed:
                self._submitButton.enable()
                self._resetButton.enable()
            else:
                self._submitButton.disable()
                self._resetButton.disable()

    def _setTime(self):
        self._hourPrev = self._hour
        self._minutePrev = self._minute
        self._handleChange(self._hour, self._minute)
        self._updateButtonState()

    def _resetTime(self):
        self._hour = self._hourPrev
        self._minute = self._minutePrev
        self._timeInput.setTime(self._hourPrev, self._minutePrev)
        self._updateButtonState()

    def _createContent(self):
        self._timeInput = TimeInput(
            self, hour=self._hour, minute=self._minute, handleChange=self._onTimeChange)
        self._timeInput.pack(side=tk.TOP)

        buttonFrame = tk.Frame(self)
        buttonFrame.pack(side=tk.BOTTOM)

        self._submitButton = StatefulButton(
            buttonFrame, label="Set", handleClick=self._setTime)
        self._submitButton.pack(side=tk.LEFT)

        self._resetButton = StatefulButton(
            buttonFrame, label="Reset", handleClick=self._resetTime)
        self._resetButton.pack(side=tk.RIGHT)
        self._updateButtonState()


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
