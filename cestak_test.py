import tkinter as tk
import calendar

okno = tk.Tk()
okno.title("Test")
tk.Label(okno, text="ok").pack(padx=20, pady=20)
okno.mainloop()

"""cal = calendar.Calendar(firstweekday=0)
tydny = cal.monthdatescalendar(2026,3)
for tyden in tydny:
    print(tyden)"""