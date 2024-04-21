import socketserver
import json
import threading
import os
from dotenv import load_dotenv

class OccupancyTCPHandler(socketserver.BaseRequestHandler):
    """
    Request handler for TCP connections that processes incoming data 
    and sends responses back to the client.
    """
    lock = threading.Lock()

    def handle(self):
        """Process incoming TCP data, decode it, and perform requested actions."""
        try:
            self.data = self.request.recv(1024).strip()
            request = json.loads(self.data.decode('utf-8'))

            method = request.get("method")
            params = request.get("params")

            if method == "update":
                response = self.update_occupancy(params)
            elif method == "get":
                response = self.send_occupancy()
            else:
                response = {"error": "Invalid method request."}
            
            self.request.sendall(json.dumps(response).encode('utf-8'))
        except json.JSONDecodeError:
            response = {"error": "Error decoding JSON from client"}
            self.request.sendall(json.dumps(response).encode('utf-8'))
        except KeyError:
            response = {"error": "Invalid data format received, expected method and params"}
            self.request.sendall(json.dumps(response).encode('utf-8'))
        except Exception as e:
            response = {"error": f"An error occurred: {e}"}
            self.request.sendall(json.dumps(response).encode('utf-8'))

    def update_occupancy(self, params):
        """
        Update the occupancy grid based on the provided parameters.

        Args:
            params (list): A list containing x and y coordinates and the value to update.
        """
        try:
            x, y, value = params
            if not (0 <= x < self.server.grid_size and 0 <= y < self.server.grid_size):
                raise ValueError(f"Index out of bounds. Please enter x and y between 0 and {int(os.getenv('GRID'))-1}.")
            if value not in (0, 1):
                raise ValueError("Invalid value for occupancy. Must be 0 or 1.")

            with OccupancyTCPHandler.lock:
                self.server.occupancy_grid[x][y] = value
            return {"success": "Grid updated successfully"}
        except ValueError as e:
            return {"error": str(e)}

    def send_occupancy(self):
        """Send the current state of the occupancy grid to the client."""
        with OccupancyTCPHandler.lock:
            return self.server.occupancy_grid

class OccupancyTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    A TCP server that handles incoming requests via multithreading and manages an occupancy grid.
    """
    def __init__(self, server_address, RequestHandlerClass):
        self.grid_size = int(os.getenv('GRID', 100))  # Default to 100x100 if not set
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
        print(f"Server is listening at {server_address[0]}:{server_address[1]}...")
        self.occupancy_grid = [[0]*self.grid_size for _ in range(self.grid_size)]

if __name__ == "__main__":
    load_dotenv()
    try:
        port = int(os.getenv('PORT', 9999))  # Default to port 9999 if not set
        print("Initializing server...")
        server = OccupancyTCPServer(('localhost', port), OccupancyTCPHandler)
        server.serve_forever()
    except ValueError:
        print("Invalid port number. Please check the PORT environment variable.")
    except OSError as e:
        print(f"OS error: {e} (Maybe the port {port} is already in use?)")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
