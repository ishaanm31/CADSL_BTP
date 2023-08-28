#!/bin/bash
#Written for Ubuntu 18.04
#Resolving dependencies
sudo dpkg --add-architecture i386
sudo apt update
sudo apt -y install git binutils curl libboost-dev libbz2-dev libc6:i386 libncurses5:i386 libsqlite3-dev libstdc++6:i386 python wget zlib1g-dev

#Snipersim
git clone http://snipersim.org/download/65a901707aef3e10/git/sniper.git
cd sniper
make
cd ..


