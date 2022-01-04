import threading
import asyncio as aio
import json
import time


class ControlPanel:
    wantToWrite = 0
    wantToRead = 0
    writeData = []
    readData = []
    closeConnection = False

    thread = None
    cv = threading.Condition(threading.Lock())

    ipServer = ""
    connected = False
    connectionError = False

    def _connect(self):
        print("Connecting")
        aio.run(self.__open_connection())
        print("Connection closed")

    async def __open_connection(self):
        self.cv.acquire()
        print("inside handler")
        try:
            reader, writer = await aio.open_connection(self.ipServer, 8899)
            self.connected = True
            self.cv.notify()
            while not self.closeConnection:
                self.cv.wait()
                if reader.at_eof():
                    self.closeConnection = True
                while self.wantToWrite > 0:
                    writer.write(self.writeData.pop(0))
                    await writer.drain()
                    self.wantToWrite = self.wantToWrite - 1
                while self.wantToRead > 0:
                    self.readData.append(await reader.readline())
                    self.wantToRead = self.wantToRead - 1
                self.cv.notify()
            writer.write_eof()
            self.connected = False
        except Exception as e:
            print(e)
            self.connectionError = True
            self.cv.notify()
            self.cv.release()

    UPLOAD = "u"
    CONTROL = "c"

    LIST_AVAILABLE = "LIST_AVAILABLE"
    LIST_ACTIVE = "LIST_ACTIVE"
    START = "START"
    STOP = "STOP"
    GET_OUTPUT = "GET_OUTPUT"

    def connect(self, ip_add) -> bool:
        if self.connected:
            return True
        self.closeConnection = False
        self.connectionError = False
        self.ipServer = ip_add
        self.thread = threading.Thread(target=self._connect)
        self.thread.start()
        self.cv.acquire()
        self.cv.wait_for(lambda: self.connectionError or self.connected)
        if self.connectionError:
            self.thread.join()
            self.cv.release()
            return False
        return True

    def disconnect(self):
        self.closeConnection = True
        self.cv.notify()
        self.cv.release()
        self.thread.join()

    def send(self, type, arg1='', arg2=''):
        self.wantToWrite = self.wantToWrite+1
        if type != 'c' and type != 'u':
            print("Error on command. Sending none")
            return
        if type == 'c':
            if arg2 != '':
                arg2 = ' '+arg2
            msg = f"{type}!!!2337###{arg1}{arg2}\n"
        else:
            msg = f"{type}!!!2337###{arg1}!!!2337###{arg2}\n"
        m = msg.encode()
        print(f"sending: {m}")
        self.writeData.append(m)
        self.cv.notify()

    def read(self):
        c = self.wantToRead
        self.wantToRead = self.wantToRead+1
        self.cv.notify()
        self.cv.wait_for(lambda: c == self.wantToRead)
        res = self.readData.pop(0)
        print(f"read: {res}")
        return res.decode()

    def getAvailable(self):
        self.send(self.CONTROL, self.LIST_AVAILABLE)
        #time.sleep(2)
        str = self.read()
        obj = json.loads(str)
        return obj

    def start(self, act):
        self.send(self.CONTROL, self.START, act)
        res = self.read()
        print(res)

    def stop(self, act):
        self.send(self.CONTROL, self.STOP, act)
        res = self.read()
        print(res)

    def getOutput(self, act):
        self.send(self.CONTROL, self.GET_OUTPUT, act)
        res = self.read()
        return res

    def upload(self, act, fileStr):
        fileStr = fileStr.replace("\n", "\a")
        self.send(self.UPLOAD, act, json.dumps(fileStr))
        r = self.read()
        print(r)
