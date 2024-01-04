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
            pipeout = os.open(constants.HTTP_SERVER2CLIENT, os.O_WRONLY)
            os.write(pipeout, str.encode(data))
        except:
            print("error writing to pipe")
    
    def readHTTP(self):
        try:
            pipein = open(constants.HTTP_CLIENT2SERVER, 'r')
            data = pipein.readline()
            return data
        except:
            print("error reading from pipe")

if __name__ == "__main__":
    
    #try:
        sys.stdout.flush()
        sys.stdin.flush()
        
        s = Server()
        s.openHTTP()
        os.mkfifo(constants.HTTP_CLIENT2SERVER)
        pipeout = os.open(constants.HTTP_CLIENT2SERVER, os.O_WRONLY)
        os.write(pipeout, str.encode("GET"))
        print(s.readHTTP())
        s.writeHTTP("RESPONSE")
    #except:
        os.close(pipeout)
        s.closeHTTP()
