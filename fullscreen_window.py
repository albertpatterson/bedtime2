
import tkinter as tk


class FullscreenWindow(tk.Frame):
    def __init__(self, root, handleSnooze):
        super().__init__(root)

        self._root = root
        self._handleSnooze = handleSnooze
        self.hide()
        self._createContent()

    def hide(self):
        self._root.update_idletasks()
        self._root.attributes("-fullscreen", False)
        self._root.overrideredirect(False)
        self._root.geometry("0x0")

    def show(self):
        self._root.update_idletasks()
        self._root.attributes("-fullscreen", True)
        self._root.overrideredirect(True)

    def _createContent(self):
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        message = tk.Label(self, text="It''s bedtime!", font=('Arial', 50))
        message.pack(side=tk.TOP)

        button = tk.Button(self, text="Snooze 5 mins",
                           font=('Arial', 50), command=self._handleSnooze)
        button.pack(side=tk.BOTTOM)
