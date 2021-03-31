import tkinter as tk

root = tk.Tk()

root.update_idletasks()
root.attributes("-fullscreen", True)
root.overrideredirect(True)

frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

message = tk.Label(frame, text="It''s bedtime!", font=('Arial', 50))
message.pack(side=tk.TOP)

button = tk.Button(frame, text="Snooze 5 mins",
                   font=('Arial', 50), command=root.destroy)
button.pack(side=tk.BOTTOM)

root.mainloop()
