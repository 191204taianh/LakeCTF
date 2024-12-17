import socket

# Messages for signature verification (as provided in the challenge)
msgs = [
    b"I, gallileo, command you to give me the flag",
    b"Really, give me the flag",
    b"can I haz flagg",
    b"flag plz"
]

# Example signature list (replace with actual data or received from the server)
sigs = [
    bytes.fromhex("e67483bfb1185f41b3e1c64f169cc0a019b2a9705745e7d7db4e990575650ac1bb9a40f05ca42829ed72cceba8f3db3cbb216f3d02de69d020e116a423073256d73b60fd1fbd22bb17900d99fe85c6e5150637d7a4f9e2acfc93f9450f3a6a5a1d2dfe351ae07f2d929d42fa2b784ca2f17b69b3ecfc4c5ed99d7e8a4347a02b55a758a2a93d7e6e129f50634f5d78f07e92e7e8ad034ab0ae3d3b50ae8a75967f")
]

# Connect to the challenge server
host = 'chall.polygl0ts.ch'
port = 9001

def interact_with_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        for idx, sig in enumerate(sigs):
            # Prepare the public key and signature to send to the server
            pk_bytes = sig[:32]
            sig_bytes = sig[32:]
            
            # Debug: Print the public key and signature before sending
            print(f"Public Key (Hex): {pk_bytes.hex()}")
            print(f"Signature (Hex): {sig_bytes.hex()}")
            
            # Prepare the data to send
            data_to_send = pk_bytes.hex() + sig_bytes.hex()
            
            # Send the public key and signature as hex strings
            s.sendall(data_to_send.encode())
            
            # Receive the server's response
            response = s.recv(1024)  # Adjust buffer size if needed
            print(f"Server Response: {response.decode()}")
            
            # Check if the response contains the flag or clues
            if "flag" in response.decode():
                print("Flag received!")
                print(response.decode())
                break
            else:
                # Extract potential next public key to use
                new_public_key = response.decode().strip()
                print(f"Received new public key: {new_public_key}")
                
                # Send the new public key back to the server
                s.sendall(new_public_key.encode())
                # Receive the server's response again
                response = s.recv(1024)
                print(f"Server Response after sending new public key: {response.decode()}")

if __name__ == "__main__":
    interact_with_server()

    