from socket import *
import threading
import time
import os

SERVER_NAME = "127.0.0.1"
SERVER_PORT = 12000

# ==========================================
# 1. SERVER CODE (Runs in a background thread)
# ==========================================
def run_server():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Allow immediate reuse of the port after stopping the script
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind((SERVER_NAME, SERVER_PORT))
    serverSocket.listen(1)
    print("[SERVER] Ready to receive connection requests...")

    while True:
        try:
            connectionSocket, addr = serverSocket.accept()
            # Receive filename from client
            filename = connectionSocket.recv(1024).decode()
            print(f"[SERVER] Client requested file: '{filename}'")
            
            # Check if file exists to prevent crashing
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    file_contents = file.read(1024)
                connectionSocket.send(file_contents.encode())
            else:
                connectionSocket.send("Error: File not found on server.".encode())
                
            connectionSocket.close()
        except Exception as e:
            print(f"[SERVER] Error encountered: {e}")
            break

# ==========================================
# 2. CLIENT CODE (Runs in the main thread)
# ==========================================
def run_client():
    # Prompt user to input a file name
    filename_input = input("\n[CLIENT] Enter file name to request: ")

    clientSocket = socket(AF_INET, SOCK_STREAM)
    try:
        clientSocket.connect((SERVER_NAME, SERVER_PORT))
        # Send the requested file name
        clientSocket.send(filename_input.encode())
        
        # Receive the file contents back
        response = clientSocket.recv(1024).decode()
        print(f"\n[CLIENT] --- Response From Server --- \n{response}\n---------------------------------")
    except Exception as e:
        print(f"[CLIENT] Connection failed: {e}")
    finally:
        clientSocket.close()

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    # Create a dummy test file so you have something to request immediately
    test_filename = "sample.txt"
    with open(test_filename, "w") as f:
        f.write("Hello! This is the content of the requested sample file from the server.")
    print(f"-> Created a local dummy file named '{test_filename}' for testing purposes.")

    # Start Server thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Small pause to guarantee the server is up and listening before the client tries to connect
    time.sleep(0.5)

    # Run Client
    run_client()
