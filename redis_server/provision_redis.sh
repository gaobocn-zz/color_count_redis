#!/bin/bash

apt-get update
apt-get install build-essential tcl

# download redis
cd /tmp
curl -O http://download.redis.io/redis-stable.tar.gz
tar xzvf redis-stable.tar.gz
cd redis-stable
make
sudo make install

# config redis
mkdir -p /etc/redis
cp /tmp/redis-stable/redis.conf /etc/redis
cp ~/color_count/redis_server/redis.service /etc/systemd/system/


sudo adduser --system --group --no-create-home redis
sudo mkdir -p /var/lib/redis
sudo chown redis:redis /var/lib/redis
sudo chmod 770 /var/lib/redis

sudo systemctl start redis
sudo systemctl enable redis
