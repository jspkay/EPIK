from MainGUI import MainGUI
from server import SimpleServer
from controller import Controller
import os, json


def uploadLaboratory(name, fileStr):
    print(f"Name: {name}\nContent: {fileStr}")
    path = os.path.expanduser(f"~/ERIS/{name}")
    f = open(path, "w")
    f.write(fileStr)
    f.close()
    print("downlaod complete!")


def processData(d):
    if d[0] == 'c':  # Control
        print("Server control")
        words = d.split("!!!2337###")[1].split(" ")
        words[0] = words[0].replace("\n", "")
        if words[0] == "START":
            c.start(words[1])
            s.send("OK")
        elif words[0] == "STOP":
            l = c.stop(words[1])
            if l == 0:
                s.send("OK")
            else:
                s.send("ERROR")
        elif words[0] == "GET_OUTPUT":
            out = c.getOutput(words[1])
            s.send(out)
        elif words[0] == "LIST_ACTIVE":
            l = c.getActive()
            s.send(l)
        elif words[0] == "LIST_AVAILABLE":
            l = c.getAvailable()
            s.send(l)
    if d[0] == 'u':  # upload
        print("Downloading...")
        _, name, fileStr = d.split("!!!2337###")
        fileStr = json.loads(fileStr).replace("\a", "\n")
        uploadLaboratory(name, fileStr)
        s.send("OK")


if __name__ == '__main__':
    ## Server setup
    s = SimpleServer()
    ## Main GUI setup
    mg = MainGUI(s.getServerIp(), False)
    ## Controller
    c = Controller()
    lastState = None
    ## Endless cycle
    while True:
        if not mg.alive:
            exit()
        t = s.isClientConnected()
        if t != lastState:
            if t:
                mg.connected(s.getClientIP())
                lastState = t
            else:
                mg.disconnected()
                lastState = t
        d = s.getData()
        if d is not None:
            processData(d)
