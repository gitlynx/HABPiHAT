% HAB Mini

# HAB Mini application
This application implements a demo setup to send and receive Data via AFSK (using Direwolf)

The ./start.sh script prepares the python virtual environment and downloads all modules that are
listed in requirements.txt. This requires network/internet access for this step. This is only 
required at installation. 

Data is sourced from serial interface.
It's not required that this application is running on the same device as direwolf. Connection
is made via a TCP socket

Data is transmitted at the rate it's received via the serial interface.

# Server 
./start.sh --server 192.168.1.62 8001 

# Client
/start.sh --client 192.168.1.56 8001