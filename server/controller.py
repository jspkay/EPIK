import subprocess as sp
import os


class Controller:
    taskList = {}
    available = []

    path = os.path.expanduser("~/ERIS")

    def getAvailable(self):
        self.available = os.listdir(self.path)
        return self.available

    def start(self, strLab):
        if strLab in self.available:
            path = os.path.expanduser(f"~/ERIS/{strLab}")
            self.taskList[strLab] = sp.Popen(["python", path],
                                             stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.PIPE)
            print("Started...")
        else:
            print("Doesn't exist")

    def stop(self, str):
        t = self.taskList[str]
        t.kill()
        return t.poll()

    def getOutput(self, strLab, input=""):
        out = None
        err = None
        try:
            out, err = self.taskList[strLab].communicate(input=input, timeout=5)

        except sp.TimeoutExpired as e:
            print("Function never returned")
            return None


        out = self.taskList[strLab].stdout.read()
        out = out + self.taskList[strLab].stderr.read()
        out = out.decode()
        print(out)
        return out

    def getActive(self):
        return [*self.taskList]
