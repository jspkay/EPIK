import tkinter as tk
from GUI_interfaces.BigIpText import BigIpText
import threading

class MainGUI:
    root = None
    activeFrame = None
    alive = True

    fullscreen = False
    ready = False

    def __init__(self, ip_add, fullscreen=True):
        self.t = threading.Thread(target=self.start, args=(ip_add, fullscreen))
        self.t.start()
        print("Waiting for Tk")
        while self.ready is False:
            pass
        print("initial setup")
        #self.disconnected(ip_add)
        self.activeFrame = BigIpText(self.root, ip_add, bg="black")
        self.activeFrame.pack(fill=tk.BOTH, expand=1)
        print("Waiting for connection...")

    def destroy(self):
        self.t.join(timeout=0.1)

    def start(self, ip_add, fullscreen=True):
        self.root = tk.Tk()
        self.fullscreen = fullscreen
        self.frame = tk.Frame(self.root, bg='black')
        self.root.bind_all("<Escape>", lambda e: exit())
        self.root.attributes("-fullscreen", self.fullscreen)
        self.ready = True
        self.root.mainloop()
        self.alive = False

    def connected(self, ip_add):
        self.activeFrame.serverIpGreen(True)
        self.activeFrame.insertClientIp(ip_add)

    def disconnected(self):
        self.activeFrame.serverIpGreen(False)
        self.activeFrame.removeClientIp()

if __name__ == '__main__':
    l = MainGUI("127.0.0.1", False)
    l.connected("192.168.1.1")