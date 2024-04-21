# Occupancy Grid Management System
This repository contains a client-server application where clients represent occupancy sensors, capable of sending occupancy data points and requesting aggregated occupancy data. The server stores these data points and provides the aggregated occupancy data as a 2D array upon request. New data points from clients should overwrite old values on the server for the same coordinates.

## 1. Application Overview

This application consists of a server and a client that manage and interact with an occupancy grid. The server maintains a 100x100 grid that tracks occupancy status (either 0 for empty or 1 for occupied) at various coordinates. Clients can update the status of specific coordinates and request the current state of the entire grid.

### Components

- **Server**: Manages the occupancy grid and processes requests from clients.
- **Client**: Sends requests to update grid data and to retrieve the current grid state.

## 2. Environment Setup and Dependencies

### Prerequisites

- OS: Ubuntu 22.04 LTS (Recommeded)
- Python 3.6 or higher
- pip (Python package installer)

### Dependencies

Most of the required packages used in this repository comes with the installation of python itself. Only one package requires to be installed with pip:

```bash
pip install python-dotenv
```


### Configuration
Clone this repository,

```bash
git clone https://github.com/Ahmed-Mujtaba-98/occupancy-grid-managment.git
cd occupancy-grid-managment/
```

Create a `.env` file in the same directory as your scripts with the following content:

```bash
PORT=5000      # Port number the server will listen on
IP=localhost   # IP address of the server (use 'localhost' for local server)
GRID=99        # Size of the 0-indexed grid (100x100 grid)
```

## 3. Running the code

### Server
Open terminal, start the server:
```bash
python server.py
```
This will initiate the server on the specified `PORT`, listening for connections from clients.

### Client

The client will connect to the server using the IP and PORT specified in the `.env` file. Use the menu prompts to interact with the server:

1. Get data: Retrieves and displays the current occupancy grid.
2. Send data: Prompts for `x`, `y` coordinates and a `value` to update in the grid.

#### Sensor 1

In another terminal, start the client:

```bash
python client.py
```

#### Sensor 2
In another terminal, start the client:

```bash
python client.py
```

## 4. Running the example
The example code in the `occupancy-grid-managment/example` folder contains hardcoded values for the occupancy at specific coordinate(s) for clients, i.e., [sensor 1](./example/sensor_one.py) and [sensor 2](./sensor_two.py), and communicate with the [server](./example/server.py).

Open terminal and head to the `occupancy-grid-managment/example`,

```bash
cd occupancy-grid-managment/example
```

Start the server:

```bash
python server.py
```

Open another terminal and start the sensor 1,

```bash
python sensor_one.py
```

Then, run the sensor 2,

```bash
python sensor_two.py
```

## 5. Advanced Setup [Docker]
Follow this [guide](./docker/README.md) to containerize this application.


Thanks, Happy Coding!
