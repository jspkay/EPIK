import tkinter as tk
import ControlPanel as cp
import tkinter.simpledialog as dialog


class ControlPanelGUI:
    root = None
    statusLabelText = None
    statusLabel = None
    activityList = None
    currentActivity = None

    connectMenu = None

    activities = []
    outputs = {}
    controlPanel = None

    def __init__(self, activities, controlpanel=None):
        self.root = tk.Toplevel()
        self.root.title("EPIK' Control Panel")
        self.root.geometry("500x500")

        self.controlPanel = cp.ControlPanel() if controlpanel is None else controlpanel

        self.activities = activities

        ## Bottom bar
        statusFrame = tk.Frame(self.root, bg="black")
        self.statusLabelText = tk.StringVar(statusFrame, "disconnected", "STATUS")
        self.statusLabel = tk.Label(statusFrame,
                               textvariable=self.statusLabelText,
                               fg="black")
        self.statusLabel.pack(side=tk.RIGHT)
        statusFrame.pack(expand=False, fill=tk.X, side=tk.BOTTOM)

        ## Main frame
        mainFrame = tk.Frame(self.root, bg="yellow")
        mainLabels = tk.Label(mainFrame)
        availableLabel = tk.Label(mainLabels, text="Available:")
        availableLabel.pack(side=tk.LEFT)

        mainLabels.pack(side=tk.TOP, expand=False, fill=tk.X)

        self.activityList = tk.Listbox(mainFrame)
        for (i, a) in enumerate(activities):
            self.activityList.insert(i, a)
        self.activityList.bind("<<ListboxSelect>>", self.changeActivity)
        self.activityList.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        activityControlBox = tk.Frame(mainFrame)
        self.activityStatusLabelText = tk.StringVar(activityControlBox,
                                           "Not running", "ACT_STATUS")
        self.activityStatusLabel = tk.Label(activityControlBox,
                                       textvariable=self.activityStatusLabelText,
                                       fg="black" )
        self.activityStatusLabel.pack(side=tk.TOP, fill=tk.X, expand=False)

        buttonFrame = tk.Frame(activityControlBox)
        self.startButton = tk.Button(buttonFrame, text="Start")
        self.startButton.bind("<Button>", self.startActivity)
        self.startButton.pack(side=tk.LEFT)
        stopButton = tk.Button(buttonFrame, text="Stop")
        stopButton.bind("<Button>", self.stopActivity)
        stopButton.pack(side=tk.LEFT)
        buttonFrame.pack(side=tk.TOP)

        self.activityLogBox = tk.Text(activityControlBox, state=tk.DISABLED)
        self.activityLogBox.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        activityControlBox.pack(expand=True, fill=tk.BOTH,side=tk.LEFT)

        mainFrame.pack(expand=True, fill=tk.BOTH)

        ## Menubar
        menubar = tk.Menu(self.root)

        self.connectMenu = tk.Menu(menubar)
        self.connectMenu.add_command(label="Connect...", command=self.connect)
        self.connectMenu.add_command(label="Disconnect", command=self.disconnect)
        self.connectMenu.add_command(label="Refresh activities", command=self.refreshAvailable)
        menubar.add_cascade(label="Connection", menu=self.connectMenu)

        self.root.config(menu=menubar)

    def getControlPanel(self):
        return self.controlPanel

    def connect(self):
        ip_add = dialog.askstring('IP', "Insepikci l'ip di EPIK")

        if self.controlPanel.connect(ip_add):
            self.statusLabelText.set(f"connected ({ip_add})")
            self.statusLabel.config(fg="green")
            self.refreshAvailable()
        else:
            self.statusLabelText.set(f"Connection refused ({ip_add})")
            self.statusLabel.config(fg="red")

    def refreshAvailable(self):
        available = self.controlPanel.getAvailable()
        for i in range(len(self.activities)):
            self.activityList.delete(0)
        for (i, a) in enumerate(available):
            self.activityList.insert(i, a)
        self.activities = available

    def disconnect(self):
        self.controlPanel.disconnect()
        self.statusLabelText.set(f"Disconnected")
        self.statusLabel.config(fg="black")

    def startActivity(self, e=None):
        self.controlPanel.start(self.currentActivity)
        out = self.controlPanel.getOutput(self.currentActivity)
        self.setLogBox(out)

    def stopActivity(self, e=None):
        self.controlPanel.stop(self.currentActivity)
        out = self.controlPanel.getOutput(self.currentActivity)
        self.setLogBox(out)

    def changeActivity(self, e=None):
        newIndex = int(e.widget.curselection()[0])
        self.currentActivity = self.activities[newIndex]
        try:
            self.setLogBox(self.outputs[self.currentActivity])
        except KeyError:
            self.setLogBox(f">>{newIndex} - {self.currentActivity}")
        print(self.activities)

    def setLogBox(self, string):
        self.activityLogBox.config(state=tk.NORMAL)
        self.activityLogBox.delete("0.1", tk.END)
        self.activityLogBox.insert("0.1", string)
        self.activityLogBox.config(state=tk.DISABLED)

if __name__ == '__main__':
    root = tk.Tk()
    c = ControlPanelGUI(["sr", "tts", "cb"])
    root.mainloop()
