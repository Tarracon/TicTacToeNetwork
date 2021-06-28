import socket
import _thread

host = ''
## Port to interface on
port = 13037

### Function to play new TicTacToe Game with a new client
def newClient(connection, addr):

    command = "BEGIN"
    gameover = False
    firstmove = "HUMAN"

    ### Initialize Board
    board = [ ['-', '-', '-'],
         ['-', '-', '-'],
         ['-', '-', '-'] ]
    
    ### Receive inital msg from client
    message = connection.recv(port).decode()
    response = commandDecoder(message, firstmove, board, gameover)
    ### Send msg to client
    connection.send(response.encode())
        
    with connection:
        ## While client hasn't QUIT and game isn't over
        while (command != "QUIT"):
            ## Receive inputted command from client
            command = connection.recv(port).decode()
            
            ### Print command for debuggin purposes
            print(command)
            ## Decipher received Command to determine response
            response = commandDecoder(command, firstmove, board, gameover)
            print(board)
            
            ## If command is PUT check for victor and game isnt over
            if(command[0] == 'P' and command[1] == 'U' and command[2] == 'T'):
                if(check_tie(board) == True):
                    response = "TIE"
                    gameover = True
                
                elif(check_for_winner('O', board) == True):
                    response = "VICTORY O"
                    gameover = True
                
                elif(check_for_winner('X', board) == True):
                    response = "VICTORY X"
                    gameover = True
                    
            ## Send response to client        
            connection.send(response.encode())
        ## Close connection
        connection.close()

def printBoard(board):
    for row in range(0,3):
        for col in range(0,3):
            printed += str(board[row][col]) + " "
    
    return printed 

## Function to reset board to default
def resetBoard(board, gameover):
    for row in range(0,3):
        for col in range(0,3):
            board[row][col] = '-'

## Simple function AI 
def AIPiece(board):
    for row in range(0,3):
        for col in range(0,3):
            if(board[row][col] == '-'):
                change1 = row
                change2 = col
    ## AI places piece in last available place
    board[change1][change2] = 'X'

## Place piece designated by client on board
def placePiece(x, y, board):
    if(board[int(x)][int(y)] == '-'):
        board[int(x)][int(y)] = 'O'
        return 0
    
    else:
        return 1

def check_for_winner(piece, board):
  ### Check for all victory conditions
  ### Three in a row
  for row in range(3):
    if(board[row][0] == piece and board[row][1] == piece and board[row][2] == piece):
      return True
  
  ### Three in a column
  for column in range(3):
    if(board[0][column] == piece and board[1][column] == piece and board[2][column] == piece):
      return True

  ### Three in a diagonal(\)
  if(board[0][0] == piece and board[1][1] == piece and board[2][2] == piece):
    return True
  ### Three in a diagonal(/)
  if(board[0][2] == piece and board[1][1] == piece and board[2][0] == piece):
    return True

  ## If any victory conditions aren't met false
  return False

def check_tie(board):
  for row in range(3):
    for column in range(3):
      if(board[row][column] != 'O' and board[row][column] != 'X'):
        return False
  
  return True

## Function to decode command decoder
def commandDecoder(command, firstmove, board, gameover):
    ## Base on command execute appropriate function
    if(command == "QUIT"):
        response = "Quiting Game"
        gameover = True
        return response

    elif(command == "HUMAN"):
        response = "Enter a Valid Move"
        return response

    elif(command == "AI"):
        AIPiece(board)
        response = "AI MOVED FIRST"
        firstmove = "AI"
        return response

    elif(command[0] == 'P' and command[1] == 'U' and command[2] == 'T'):
        ##Improper format of PUT command
        if(len(command) != 6):
            print(len(command))
            response = "Please Enter Command in Form: PUT XX"
            return response

        elif(gameover == False):
            print("Reached")
            row = command[4]
            column = command[5]
            placed = placePiece(row, column, board)
            ## If piece successfully placed 
            if(placed == 0):
                if((check_for_winner('O', board) == False) and check_tie(board) == False):
                    AIPiece(board)
                    response = "OK"
                    return response
            ## Else piece unsuccessfully placed
            else:
                response = "Space is already used"
                return response

        else:
            response = "GAME OVER"
            return response
                
    
    elif(command == "NEW"):
        resetBoard(board, gameover)
        gameover = False
        response = "New Game Started"

        if(firstmove == "AI"):
            AIPiece()

        return response

    ## Else command is invalid
    else:
        response = "Please Enter an Valid Comnmand"
        return response


def main():
    ## Create socket
    Server = socket.socket()
    ## Bind host to port
    Server.bind((host, port))
    ## Listen for client connections
    Server.listen(10)

    while True:
        ## Accept new connection
        connection, address = Server.accept()
        ## Start new thread for incoming connections
        _thread.start_new_thread(newClient,(connection,address))

    ## Close socket
    Server.close()
  

### Call main when script ran
if __name__ == "__main__":
    try:
        main()

    ##If user pushes CTRL-C, exit safely
    except KeyboardInterrupt:
        exit()
        

