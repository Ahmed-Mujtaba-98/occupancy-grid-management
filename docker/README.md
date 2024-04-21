# Advanced Setup [Docker]
The overall occupancy-grid-management application is containerized into one docker image, therefore, use atleast one container as a server, and other as many containers as clients, i.e., sensors.

To run the occupancy-grid-management application inside the docker container, you can,

- Create your docker image locally and enter inside the container to run the client/server code.
- Pull the pre-compiled image from the docker hub and enter inside the container to run the client/server code.

For each choice, there is shell scipt provided in the `occupancy-grid-managment/docker` folder.

**Note that all the shell scripts must be run from the parent directory, i.e., `occupancy-grid-managment/`**

## Create Local Docker Image
To create a local docker image, run,

```bash
chmod +x ./docker/setup_docker.sh    # make it executable
./docker/setup_docker.sh
```

### Run Server

Run the server container,

```bash
chmod +x ./docker/enter_container.sh    # make it executable
./docker/enter_container.sh
```

Activate the virtual environment inside the container,
```bash
. /venv/bin/activate
```

If you see the virtual environment activated, then proceed to run the `server.py`,

```bash
python server.py
```

### Run Client

Open another terminal and create another container,
```bash
./docker/enter_container.sh
```

Activate the virtual environment inside the container,
```bash
. /venv/bin/activate
```

and run client,

```bash
python client.py
```
## Pull Docker Image From DockerHub

1. Pull the image from DockerHub,

```
docker pull ahmed709/occupancy-grid:latest
```

2. Run the image,

```
docker run -t -d --name occupancy-container ahmed709/occupancy-grid:latest
```

3. Run the container,

```
docker exec -it occupancy-container ash
````

Use atleast one container to run the server, and other as clients.
