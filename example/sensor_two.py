import socket
import json
import re
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


if __name__ == "__main__":
    load_dotenv()
    port, IP = int(os.getenv('PORT')), os.getenv('IP')

    # Example use of the send_data function to update and retrieve occupancy data
    send_data(IP, port, "update", [2, 1, 1])
    send_data(IP, port, "update", [2, 2, 1])
    send_data(IP, port, "update", [3, 1, 0])
    send_data(IP, port, "update", [3, 2, 0])

    send_data(IP, port, "get", [])


