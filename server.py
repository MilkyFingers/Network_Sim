import os, sys
import constants

class Server:

    def __init__(self):
        self.ip = constants.SERVER_IP
        self.name = constants.SERVER_NAME
        self.log = constants.SERVER_LOGS

    def openHTTP(self):
        # opens an os pipe for http communication - so named in the constant file
        if not os.path.exists(constants.HTTP_SERVER2CLIENT):
            os.mkfifo(constants.HTTP_SERVER2CLIENT)

    def closeHTTP(self):
        # close the http pipe
        try:
            os.remove(constants.HTTP_SERVER2CLIENT)
        except:
            print("error closing pipe")

    def writeHTTP(self, data):
        try:
            with open(constants.HTTP_SERVER2CLIENT, "w") as pipe:
                pipe.write(data)
        except:
            print("error writing to pipe")
    
    def readHTTP(self):
        try:
            with open(constants.HTTP_CLIENT2SERVER, 'r') as pipe:
                data = pipe.readline()
                return data
        except:
            print("error reading from pipe")

if __name__ == "__main__":
    
    s = Server()
    s.openHTTP()

    while True:
        try:
            if os.path.exists(constants.HTTP_CLIENT2SERVER):
                data = s.readHTTP()
                if data == "QUIT":
                    s.writeHTTP("303: Closed connection successfully")
                    raise KeyboardInterrupt
                else:
                    s.writeHTTP("RESPONSE")

        except KeyboardInterrupt:
            s.closeHTTP()
            break