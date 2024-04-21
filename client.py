import socket
import json
import os
from dotenv import load_dotenv

def send_data(host, port, method, params):
    """
    Send data to the server and handle the response.

    This function connects to the server at the given host and port, sends a request
    specified by the method and parameters, and handles the response appropriately.

    Args:
        host (str): The server's hostname or IP address.
        port (int): The port number on which the server is listening.
        method (str): The method of the request ("update" or "get").
        params (list): The parameters of the request. This is typically a list that
                       includes coordinates and possibly a value, depending on the method.

    Returns:
        None
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        message = json.dumps({"method": method, "params": params})
        sock.sendall(message.encode('utf-8'))
        
        if method == "get":
            chunks = []
            while True:
                chunk = sock.recv(4096)  # Read 4096 bytes
                if not chunk:
                    break
                chunks.append(chunk)
            response = b''.join(chunks).decode('utf-8')
            occupancy_grid = json.loads(response)
            print("Received occupancy grid:")
            for row in occupancy_grid:
                print(row)
        elif method == "update":
            response = sock.recv(4096)  # Increased buffer size to ensure complete message is received
            data = json.loads(response.decode('utf-8'))
            print("Server response:", data)

def get_int_input(prompt, min_val=0, max_val=99):
    """
    Safely attempts to convert the user input into an integer. Re-prompts if the input is not valid.

    Args:
        prompt (str): The message displayed to the user requesting input.
        min_val (int): Minimum acceptable value for input.
        max_val (int): Maximum acceptable value for input.

    Returns:
        int: The user input converted to an integer.
    """
    max_val = int(os.getenv('GRID')) - 1
    while True:
        input_value = input(prompt)
        if not input_value.isdigit() or not (min_val <= int(input_value) <= max_val):
            print(f"Invalid input. Please enter an integer between {min_val} and {max_val}.")
        else:
            return int(input_value)

def main():
    load_dotenv()
    port, IP = int(os.getenv('PORT')), os.getenv('IP')

    while True:
        print("\nMenu:")
        print("1. Get data")
        print("2. Send data")
        print("3. Exit")
        choice = input("Choose from 1/2/3: ")

        if choice == '1':
            send_data(IP, port, "get", [])
        elif choice == '2':
            x = get_int_input(f"Enter X coordinate (0-{int(os.getenv('GRID'))-1}): ")
            y = get_int_input(f"Enter Y coordinate (0-{int(os.getenv('GRID'))-1}): ")
            value = get_int_input("Enter value (0 or 1): ", min_val=0, max_val=1)
            send_data(IP, port, "update", [x, y, value])
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice, choose from 1/2/3.")

if __name__ == "__main__":
    main()
