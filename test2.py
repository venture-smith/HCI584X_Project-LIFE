# https://www.delftstack.com/howto/python-tkinter/how-to-switch-frames-in-tkinter/
# Multi-frame tkinter application v2.3
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.scrolledtext as tkst
# import sqlite3 # Bring this back in if we end up using a database for a webapp.
from tkinter import messagebox as msgbox
from PIL import ImageTk, Image
import fileinput # May not need this module - imported from a different application.
from lookup import *

CountIteration = 1

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is the start page").pack(side="top", fill="x", pady=10)
        tk.Label(self, text="Count").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Open page one",
                  command=lambda: master.switch_frame(PageOne)).pack()
        tk.Button(self, text="Open page two",
                  command=lambda: master.switch_frame(PageTwo)).pack()
        tk.Button(self, text="Open page three",
                  command=lambda: master.switch_frame(PageThree)).pack()

class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page one").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Next",
                  command=lambda: master.switch_frame(PageTwo)).pack()

class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        global CountIteration
        CountIteration +=1
        print(CountIteration)
        test = StringVar()
        test.set("Count:" + str(CountIteration))        
        
        tk.Label(self, textvariable =test).pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Previous",
                  command=lambda: master.switch_frame(PageOne)).pack()
        tk.Button(self, text="Re-run",
                  command=lambda: master.switch_frame(PageTwo)).pack()
        tk.Button(self, text="Next",
                  command=lambda: master.switch_frame(PageThree)).pack()
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

class PageThree(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page three").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Previous",
                  command=lambda: master.switch_frame(PageTwo)).pack()
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()