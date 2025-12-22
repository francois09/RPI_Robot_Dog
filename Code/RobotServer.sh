#!/bin/sh

# Setup new run program
cp /opt/RPI_Robot_Dog/Code/RobotServer.sh ~/
chmod +x ~/RobotServer.sh

# Update repository with recent version
cd /opt/RPI_Robot_Dog/Code/Server
python Progress.py fetch
git fetch origin

python Progress.py pull
git pull

# Then prepare and run the server
python Progress.py start

cp ~/point.txt .
cp ~/params.json .
python main.py -tn
python Progress.py stop
