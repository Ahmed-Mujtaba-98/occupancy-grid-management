#!/bin/sh

docker build -f docker/Dockerfile -t main .
docker run -t -d --name main main