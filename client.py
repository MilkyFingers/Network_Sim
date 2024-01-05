import os
import constants
from server import Server

class Client:
    def __init__(self):
        self.ip = constants.CLIENT_IP

    def openHTTP(self):
        if not os.path.exists(constants.HTTP_CLIENT2SERVER):
            os.mkfifo(constants.HTTP_CLIENT2SERVER)

    def closeHTTP(self):
        try:
            os.remove(constants.HTTP_CLIENT2SERVER)
        except:
            print("Error closing server connection")

    def writeHTTP(self, data):
        try:
            with open(constants.HTTP_CLIENT2SERVER, "w") as pipe:
                pipe.write(data)
        except:
            print("Error sending request to server")
    
    def readHTTP(self):
        try:
            with open(constants.HTTP_SERVER2CLIENT, "r") as pipe:
                data = pipe.read()
                return data
        except:
            print("Error recieving response from server")
    
    def log(self, data):
        try:
            with open(constants.CLIENT_LOGS, "a") as f:
                f.write(data + "\n")
        except:
            print(f"Failed to log data. Data: {data}")
        
if __name__ == "__main__":
    
    c = Client()
    c.openHTTP()

    while True:
        try:
            usinp = input(">>> ")
            c.log(usinp)
            c.writeHTTP(usinp)
            data = c.readHTTP()
            print(data)
            c.log(data + "\n")
            if usinp == "QUIT":
                raise KeyboardInterrupt

        except KeyboardInterrupt:
            c.closeHTTP()
            break