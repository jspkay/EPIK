import tkinter as tk
import tkinter.font as tkFont

class BigIpText(tk.Frame):
    ipLabel = {"size": 0}
    ipConnLabel = {}

    def __init__(self, parent, ip_add="", **kwargs):
        tk.Frame.__init__(self, **kwargs)
        self.parent = parent

        self.pack(fill=tk.BOTH, expand=1)
        self.rowconfigure(0, weight=10)
        self.columnconfigure(0, weight=1)
        self.bind("<Configure>", self.setFontSize)

        self.ipLabel["str"] = tk.StringVar()
        self.ipLabel["str"].set(ip_add)

        self.ipLabel["font"] = tkFont.Font(family="Courier New", size=self.ipLabel["size"])

        self.ipLabel["obj"] = tk.Label(self,
                                       textvariable=self.ipLabel["str"],
                                       font=self.ipLabel["font"],
                                       fg="white", bg="black")

        self.ipLabel["obj"].grid(row=0, column=0, padx=20, pady=20)

    def setFontSize(self, e=None):
        new_size = -max(12, int(self.winfo_height() / 10))
        self.ipLabel["font"].configure(size=new_size)
        try:
            self.ipConnLabel["font"].configure(size=int(new_size * .8))
        except KeyError as e:
            print(f"key {e} is not present yet")

    def serverIpGreen(self, isIt):
        self.ipLabel["obj"].configure(fg="green" if isIt else "white")

    def insertClientIp(self, ip_add):
        self.ipConnLabel["str"] = tk.StringVar()
        self.ipConnLabel["str"].set("(" + ip_add + ")")
        self.ipConnLabel["font"] = tkFont.Font(family="courier New")
        self.ipConnLabel["size"] = self.ipLabel["size"] * 0.5
        self.ipConnLabel["obj"] = tk.Label(self,
                                           textvariable=self.ipConnLabel["str"],
                                           font=self.ipConnLabel["font"],
                                           fg="white", bg="black")
        self.ipConnLabel["obj"].grid(row=1, column=0)

    def removeClientIp(self):
        try:
            self.ipConnLabel["obj"].destroy()
        except KeyError as e:
            print("not created yet")