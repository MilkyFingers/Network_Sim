import os, sys
import constants
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE,SIG_DFL) 

class Server:

    def __init__(self):
        self.ip = constants.SERVER_IP
        self.name = constants.SERVER_NAME
        self.log = constants.SERVER_LOGS
        self.HTTP_OPEN = False

    def openHTTP(self):
        # opens an os pipe for http communication - so named in the constant file
        if not os.path.exists(constants.HTTP_SERVER2CLIENT):
            os.mkfifo(constants.HTTP_SERVER2CLIENT)
            self.HTTP_OPEN = True

    def closeHTTP(self):
        # close the http pipe
        try:
            os.remove(constants.HTTP_SERVER2CLIENT)
            self.HTTP_OPEN = False
        except:
            print("error closing pipe")

    def writeHTTP(self, data):
        try:
            if self.HTTP_OPEN:
                with open(constants.HTTP_SERVER2CLIENT, 'w') as pipeout:
                    pipeout.write(data)
            else:
                print("There is no open pipe!")
        except:
            print("error writing to pipe")
    
    def readHTTP(self):
        try:
            with open(constants.HTTP_CLIENT2SERVER, "r") as pipein:
                return pipein.read()
        except:
            print("error reading from pipe")

    def cleanHTTPpipes(self):
        try:
            os.remove(constants.HTTP_SERVER2CLIENT)
        except:
            pass

if __name__ == "__main__":

    os.remove(constants.HTTP_CLIENT2SERVER)

    os.mkfifo(constants.HTTP_CLIENT2SERVER)
    s = Server()
    s.openHTTP()

    count = 0

    while count < 5:

        # first write from client
        with open(constants.HTTP_CLIENT2SERVER, "w") as pipeoutclient:
            pipeoutclient.write("GET")

        print(s.readHTTP())

        s.writeHTTP("response")

        with open(constants.HTTP_SERVER2CLIENT, 'r') as pipeinclient:
            print(pipeinclient.read())

        count += 1

    s.closeHTTP()
    #os.remove(constants.HTTP_CLIENT2SERVER)



        