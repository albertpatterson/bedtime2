
import tkinter as tk


class FullscreenWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self._root = root
        self._configureTopLevel()
        self._createContent()

    def _configureTopLevel(self):
        self._root.geometry("0x0")
        self._root.update_idletasks()
        self._root.attributes("-fullscreen", True)
        self._root.overrideredirect(True)

    def _createContent(self):
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        message = tk.Label(self, text="It''s bedtime!", font=('Arial', 50))
        message.pack(side=tk.TOP)

        button = tk.Button(self, text="Snooze 5 mins",
                           font=('Arial', 50), command=self._root.destroy)
        button.pack(side=tk.BOTTOM)
