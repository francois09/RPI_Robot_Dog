#!/bin/sh

# Update repository with recent version
cd /opt/RPI_Robot_Dog
git fetch origin
git pull

# Then prepare and run the server
cd Code/Server
cp ~/point.txt .
cp ~/params.json .
sudo python main.py -tn
