#!/bin/sh

# Update repository with recent version
cd /opt/RPI_Robot_Dog
sudo python Code/Server/Progress.py fetch
git fetch origin
sudo python Code/Server/Progress.py pull
git pull

# Then prepare and run the server
sudo python Code/Server/Progress.py start
cd Code/Server
cp ~/point.txt .
cp ~/params.json .
sudo python main.py -tn
