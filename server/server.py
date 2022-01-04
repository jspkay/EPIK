import json
import netifaces as ni
import asyncio as aio
import threading


class SimpleServer:
    ip = ""
    clientIP = ""
    connected = False

    data = []
    writeData = ""
    wantToWrite = False

    t = None
    lock = threading.Lock()

    server = None
    alive = True

    def __init__(self):
        self.ip = ni.ifaddresses('wlp2s0')[ni.AF_INET][0]['addr']
        self.t = threading.Thread(target=self.start_wrapper, daemon=True)
        self.t.start()

    def start_wrapper(self):
        aio.run(self.mainloop())

    async def handle_data(self, reader, writer):
        self.clientIP = writer.get_extra_info('peername')[0]
        print(f"Client connected ({self.clientIP!r})")
        self.connected = True
        while self.connected:
            # Read connection line by line
            rec = await reader.readline()
            print(f"Received: {rec}")
            self.lock.acquire()
            if(rec != b''):
                self.data.append(rec.decode())
                print("Data ready to be processed")
            self.lock.release()
            self.connected = False if reader.at_eof() else True
            while not self.wantToWrite:
                pass
            self.lock.acquire()
            print("entered server writing loop")
            bytes = self.writeData.encode()
            writer.write(bytes)
            await writer.drain()
            print(f"writer sent {bytes}")
            self.wantToWrite = False
            self.lock.release()

    async def mainloop(self):
        print(f"server ip address is {self.ip}\n\n\n")
        self.server = await aio.start_server(self.handle_data, "127.0.0.1", 8899)
        addrs = ', '.join(str(sock.getsockname()) for sock in self.server.sockets)
        print(f'Serving on {addrs}')
        async with self.server:
            await self.server.serve_forever()

    def getServerIp(self):
        return self.ip

    def waitForData(self):
        while len(self.data) == 0:
            pass

    def getData(self):
        res = None
        if len(self.data) != 0:
            self.lock.acquire()
            res = self.data.pop(0).replace("\n", "")
            self.lock.release()
        return res

    def getClientIP(self):
        return self.clientIP

    def isClientConnected(self):
        return self.connected

    def send(self, obj):
        #print(f"sending object {obj}")
        str = json.dumps(obj)
        self.lock.acquire()
        self.writeData = str+'\n'
        self.wantToWrite = True
        self.lock.release()


if __name__ == '__main__':
    s = SimpleServer()
