import os, sys
import constants

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
        except OSError:
            print("error closing pipe")

    def writeHTTP(self, data):
        try:
            if self.HTTP_OPEN:
                with open(constants.HTTP_SERVER2CLIENT, 'w') as pipeout:
                    pipeout.write(data)
                    # every server response is logged 
                    self.log(data)
            else:
                print("There is no open pipe!")
        except OSError:
            print("error writing to pipe")
    
    def readHTTP(self):
        try:
            with open(constants.HTTP_CLIENT2SERVER, "r") as pipein:
                return pipein.read()
        except OSError:
            print("error reading from pipe")

    def log(self, data):
        with open(self.log, 'a') as logfile:
            logfile.write(data)


if __name__ == "__main__":

    s = Server()
    s.openHTTP()

    count = 0

    while count < 5:

        print(s.readHTTP())

        s.writeHTTP("response")

        count += 1

    s.closeHTTP()




        
