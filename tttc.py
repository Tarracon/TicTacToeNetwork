import socket
import sys

## Create socket
client = socket.socket()
## Port to interface on 
port = int(13037)

def main():
    
    message = "START"

    
    if(len(sys.argv) > 1):
        print(sys.argv)

        ## If only -s is passed to script connect to specified IP
        if(len(sys.argv) == 4 and sys.argv[2] == "-s"):
            host = sys.argv[3]
            client.connect((host,port))

        ## If -c is pass to script, client makes first move
        elif(sys.argv[1] == "-c" and len(sys.argv) == 2):
            client.connect(("localhost",port))
            message = "HUMAN"
            client.send(message.encode())
        
        else:
            client.connect(("localhost",port))
            message = "AI"
            client.send(message.encode())

    ##
    if(len(sys.argv) == 1):
        message = "AI"
        client.send(message.encode())

    received = client.recv(port).decode()
    print(received)

    ## While doesn't QUIT
    while (message != "QUIT"):

        ## Ask for command to input
        message = input("Enter a command: ")
        ## Send message to server
        client.send(message.encode())
        ## Receive response
        received = client.recv(port).decode()
        ## Response is VICTORY Game is Over
        if(received == "VICTORY X"):
            print("You've Lost")

        elif(received == "VICTORY O"):
            print("You've Won")

        print(received)

    ## Close connection    
    client.close()

### Call main when script ran
if __name__ == "__main__":
    try:
        main()
        
    ##If user pushes CTRL-C, exit safely
    except KeyboardInterrupt:
        exit()
