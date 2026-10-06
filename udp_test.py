from socket import *
import threading
import time
import os

SERVER_NAME = "127.0.0.1"
SERVER_PORT = 12000

# ==========================================
# 1. UDP SERVER CODE (Runs in background)
# ==========================================
def run_server():
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((SERVER_NAME, SERVER_PORT))
    print("[SERVER] The server is ready to receive")

    while True:
        try:
            # Receive filename data and the client's network address
            bytes_received, clientAddress = serverSocket.recvfrom(2048)
            filename = bytes_received.decode("utf-8")
            print(f"[SERVER] Received request for file: '{filename}' from {clientAddress}")
            
            # Check if file exists safely to prevent server crashes
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    l = file.read(2048)
                # Send file content back to client
                serverSocket.sendto(bytes(l, "utf-8"), clientAddress)
                print(f"[SERVER] Sent back to client: {l}")
            else:
                error_msg = "Error: File not found on server."
                serverSocket.sendto(bytes(error_msg, "utf-8"), clientAddress)
                
        except Exception as e:
            print(f"[SERVER] Error: {e}")
            break

# ==========================================
# 2. UDP CLIENT CODE (Runs in foreground)
# ==========================================
def run_client():
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    
    # Prompt user for input file name
    sentence = input("\n[CLIENT] Enter file name: ")
    
    # Send filename encoded as bytes to the server
    clientSocket.sendto(bytes(sentence, "utf-8"), (SERVER_NAME, SERVER_PORT))
    
    # Receive file contents back from the server
    filecontents, serverAddress = clientSocket.recvfrom(2048)
    
    # Decode and print output
    print(f"\n[CLIENT] --- From Server --- \n{filecontents.decode('utf-8')}\n-----------------------------")
    
    clientSocket.close()

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    # Create a dummy file automatically so you have a valid input to test
    test_file = "udp_test.txt"
    with open(test_file, "w") as f:
        f.write("Success! This file text was transferred using UDP sockets.")
    print(f"-> Setup: Created a local test file named '{test_file}'")

    # Start the UDP server thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Give server a moment to bind to the port
    time.sleep(0.5)

    # Launch the client sequence
    run_client()
