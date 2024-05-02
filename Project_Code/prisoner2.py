import socket
import random

DEST_IP = socket.gethostbyname(socket.gethostname())  # Server IP address
DEST_PORT = 12345  # Server port number

# Create a socket object
prisoner_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
prisoner_socket.connect((DEST_IP, DEST_PORT))

# Receive the range (L, R) and X from the server
range_data = prisoner_socket.recv(1024).decode('utf-8')
L, R, X = map(int, range_data.split(':'))

while True:
  prisoner_guess = random.randint(L, R)
  data = f'prisoner2:{prisoner_guess}'
  prisoner_socket.send(data.encode('utf-8'))
  message = prisoner_socket.recv(1024).decode('utf-8')
  print(f'message received: {message}')

  if(prisoner_guess>X):
        R=prisoner_guess-1
  elif(prisoner_guess<X):
        L=prisoner_guess+1 
  else:
       message = prisoner_socket.recv(1024).decode('utf-8')
       print(f'message received: {message}')
      # print("guess is equal to X")
       break       
       
# Close the connection
prisoner_socket.close()
if (prisoner_guess==X):
    print('Prisoner 2 has escaped!')
