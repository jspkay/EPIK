import tkinter as tk
import tkinter.messagebox as tkMessage
import os, sys, subprocess, signal
import asyncio as aio
from GUI.ControlPanelGUI import ControlPanelGUI

global labL


class LabGUI(tk.Frame):
    process = None
    p = None
    ba = None
    menuBar = None

    textEdit = None
    labs = None

    controlPanel = None

    name = ""

    def __init__(self, root, pdfFile, gotoMain, **kwargs):
        tk.Frame.__init__(self, root, kwargs)
        self.parent = root

        self.open_file(pdfFile)
        self.name = os.path.basename(pdfFile)

        ba = tk.PhotoImage(file=r"GUI/imgs/backArrow.png").subsample(3, 5)
        self.ba = ba

        # self.configure(bg="blue")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        button = tk.Button(self, image=ba, width="40", height="40", compound=tk.LEFT)
        button.grid(row=0, column=0, sticky="e")
        button.bind("<Button>", gotoMain)

        self.menuBar = tk.Menu(self.parent)

        fileMenu = tk.Menu(self.menuBar)
        fileMenu.add_command(label="Indietro", command=gotoMain)
        self.menuBar.add_cascade(label="File", menu=fileMenu)

        erisMenu = tk.Menu(self.menuBar)
        erisMenu.add_command(label="Upload", command=self.upload)
        def openControlPanel():
            ControlPanelGUI(self.labs, self.controlPanel)
        erisMenu.add_command(label="ERIS control panel", command=openControlPanel)
        self.menuBar.add_cascade(label="eris", menu=erisMenu)

        t = tk.Text(self)  # , bg="red" )
        t.grid(row=1, column=0, sticky="nswe")
        self.textEdit = t

        # t.after(100, self.showText)
        t.insert("1.0", "Insert code here...")
        t.bind("<Button>", self.firstInsertion)

        root.config(menu=self.menuBar)

    def setControlPanel(self, labs, cp):
        self.labs = labs
        self.controlPanel = cp

    def firstInsertion(self, e=None):
        self.textEdit.delete("1.0", tk.END)
        self.textEdit.unbind("<Button>")

    def showText(self, e=None):
        print(self.textEdit.get("1.0", tk.END))
        self.textEdit.after(100, self.showText)

    def upload(self):
        if not self.controlPanel.connected:
            tkMessage.showerror(title="Error", message="Connect first!")
            return
        text = self.textEdit.get("1.0", tk.END)
        self.controlPanel.upload(self.name, text)

    def open_file(self, filename):
        if sys.platform == "win32":
            # os.startfile(filename)
            self.p = subprocess.Popen([filename], shell=True)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            self.p = subprocess.Popen([opener, filename])

