import socket
import random

# Connect to the challenge server
HOST = 'chall.polygl0ts.ch'
PORT = 9068

def interact_with_server():
    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # Read initial question about circuit size
    s.recv(1024)  # Ignore the initial prompt

    # Choose a circuit size between 3 and 11 (since B = 12)
    size = random.randint(3, 11)
    s.send(f"{size}\n".encode())

    # Initializing some variables
    correct = 0
    keys = set()
    b = random.randint(0, 1)  # Randomly choose b (0 or 1)

    while correct < 32:
        # Ask for the user choice
        choice_prompt = s.recv(1024).decode()
        print(choice_prompt)
        
        # Decide whether to check the bit (option 1) or test an input (option 2)
        if 'check bit' in choice_prompt:
            s.send("1\n".encode())  # Choose to check the bit
            bit_check = s.recv(1024).decode()
            print(bit_check)

            # Assert that the server sends the correct bit
            s.send(f"{b}\n".encode())  # Send the current bit value

            # Update b for the next iteration
            b = random.randint(0, 1)
            correct += 1
            # Reset keys set after each correct check
            keys = set()
        else:
            s.send("2\n".encode())  # Choose to test an input
            input_value = random.randint(0, 2 ** 12 - 1)  # Random input within range

            if input_value in keys or len(keys) > 7:
                print("Too many keys or repeated input!")
                continue

            keys.add(input_value)

            # Send the input value to the server
            s.send(f"{input_value}\n".encode())

            # Get the response from the server
            result = s.recv(1024).decode()
            print(f"Result for input {input_value}: {result}")
    
    # After 32 correct checks, the flag is revealed
    flag = s.recv(1024).decode()
    print(f"Flag: {flag}")

    # Close the connection
    s.close()

if __name__ == "__main__":
    interact_with_server()
