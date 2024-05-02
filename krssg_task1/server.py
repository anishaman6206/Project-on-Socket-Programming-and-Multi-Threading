import socket
import threading
import random

# Server configuration
HOST_IP = socket.gethostbyname(socket.gethostname())  
HOST_PORT = 12345  
num_prisoners = 4 # Number of prisoners to handle

# Shared variables between server and clients to store the num_range (L, R) and prisoner guesses
num_range = None
X = None

lock = threading.Lock()

# Function to handle prisoner connections
def game_moderator(prisoner_socket, prisoner_address):
    global num_range, X, prisoner_guesses

    print(f'Accepted connection from {prisoner_address[0]}:{prisoner_address[1]}')

    with lock: #lock so that only 1 thread have access at a time
     if num_range is None:
            # Generate a random num_range (L, R) as per constraint
            L = random.randint(1, 10**5-10**4)
            R = L + random.randint(10**4, 10**5)
            num_range = (L, R)

     if X is None:
            # Generate a random number X between L and R
            L, R = num_range
            X = random.randint(L, R)

    # Send the num_range (L, R) and X to the prisoner
    prisoner_socket.send(f'{num_range[0]}:{num_range[1]}:{X}'.encode('utf-8'))


    print(f'num_range: {num_range}')
    print(f'Generated number X: {X}')

    with lock:
     
     while True:
      data = prisoner_socket.recv(1024).decode('utf-8')
      prisoner_name, prisoner_guess = data.split(':')
      prisoner_guess = int(prisoner_guess)
      print(f'{prisoner_name} guess: {prisoner_guess}')
      if prisoner_guess > X:
        message = 'The value is too high.'
        
      elif prisoner_guess < X:
        message = 'The value is too low.'
       
      else:
        message = 'The client has guessed the correct value.'
        break
      
    # Send message to the prisoner
      prisoner_socket.send(message.encode('utf-8'))

    # Close the connection
     prisoner_socket.close()
    
     print(f'Connection with {prisoner_address[0]}:{prisoner_address[1]} closed')
     


# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST_IP, HOST_PORT))

# Listen for incoming connections
server_socket.listen(num_prisoners)
print(f'Server listening on {HOST_IP}:{HOST_PORT}')

for i in range(num_prisoners):
    prisoner_socket, prisoner_address = server_socket.accept()
    # Start a new thread to handle the prisoner connection
    prisoner_thread = threading.Thread(target=game_moderator, args=(prisoner_socket, prisoner_address))
    prisoner_thread.start()
