import os
import constants

class Server:

    def __init__(self):
        self.ip = constants.SERVER_IP
        self.name = constants.SERVER_NAME
        self.log = constants.SERVER_LOGS

    def openHTTP(self):
        # opens an os pipe for http communication - so named in the constant file
        os.mkfifo(constants.HTTP_SERVER2CLIENT)

    def closeHTTP(self):
        # close the http pipe
        os.remove(constants.HTTP_SERVER2CLIENT)

    def writeHTTP(self, data):
        with open(constants.HTTP_SERVER2CLIENT, "w") as pipe:
            pipe.write(data)
    
    def readHTTP(self):
        with open(constants.HTTP_CLIENT2SERVER, "r") as pipe:
            data = pipe.read()
            print(data)
            return data
        
if __name__ == "__main__":
    
    s = Server()
    s.openHTTP()

    while True:

        try:
            
            data = s.readHTTP()
            s.writeHTTP("response")

        except KeyboardInterrupt:
            s.closeHTTP()
            break


    