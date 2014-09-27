#!/usr/bin/env bash

# Install packages.
apt-get update
apt-get install -y apache2 python-pip
rm -rf /var/www
ln -fs /vagrant /var/www

# Install python packages.
pip install -r requirements.txt
