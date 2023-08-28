#!/bin/bash
#Written for Ubuntu 18.04
#Resolving dependencies
sudo apt update
sudo apt -y install build-essential

#BBV generator
wget https://sourceware.org/pub/valgrind/valgrind-3.21.0.tar.bz2
tar -xf valgrind-3.21.0.tar.bz2
rm valgrind-3.21.0.tar.bz2
cd valgrind-3.21.0
./configure
make
sudo make install
cd ..

#SimPoint
make


