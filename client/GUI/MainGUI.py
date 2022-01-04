import tkinter as tk


class MainGUI(tk.Frame):
    cellsWidgets = []
    menubar = None

    def __init__(self, root, cells, cols=3, handler=None):
        tk.Frame.__init__(self, root, bg="black")
        self.parent = root

        for i in range(0, cols):
            self.grid_columnconfigure(i, weight=1, uniform=1)

        i = 0
        for f in cells:
            l = tk.Button(self, anchor="center", text=f)
            l.grid(row=int(i / 3), column=i % 3, ipadx=5, ipady=5, sticky="nswe")

            def h(e, index=i):
                handler(e, index)

            l.bind("<Button>", h)
            self.cellsWidgets.append(l)
            i = i + 1
        for j in range(0, int(i / 3)):
            self.grid_rowconfigure(j, weight=1, uniform=1)

    def getMenuBar(self):
        menubar = tk.Menu(self.parent)
        fm = tk.Menu(menubar)
        fm.add_command(label="Salva progressi...", command=None)
        fm.add_command(label="Carica progressi...", command=None)
        fm.add_separator()
        fm.add_command(label="Esci", command=self.closeProgram)

        menubar.add_cascade(label="File", menu=fm)

        return menubar

    def closeProgram(self):
        exit(self.destroy())
