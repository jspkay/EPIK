import os
import tkinter as tk
import ControlPanel
from GUI import MainGUI, LabGUI, ControlPanelGUI

labL = None
labs = os.listdir("./pdf")

def gotoMain(e=None):
    global labL
    if labL is not None:
        labL.destroy()
    mainAct.grid()

    m = mainAct.getMenuBar()
    addToolsMenu(m)
    root.config(menu=m)


def gotoLab(e, index):
    global labL
    print(e, end=" - ")
    print(e.widget, end=" - ")
    print(index)
    mainAct.grid_remove()
    # mainAct.destroy()
    labL = LabGUI.LabGUI(root, f"./pdf/{labs[index]}", gotoMain)
    labL.setControlPanel(labs, cp)
    labL.grid(row=0, column=0, sticky="nswe")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    # root.config(menu = labL.getMenuBar())


def addToolsMenu(menu):
    toolsMenu = tk.Menu(menu)
    toolsMenu.add_command(label="EPIK control panel", command=openControlPanel)
    menu.add_cascade(label="Tools", menu=toolsMenu)


def openControlPanel():
    ControlPanelGUI.ControlPanelGUI(labs, cp)


cp = ControlPanel.ControlPanel()

root = tk.Tk()
root.title("EPIK")

mainAct = MainGUI.MainGUI(root, labs, handler=gotoLab)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.geometry("400x300")

gotoMain()

root.mainloop()
