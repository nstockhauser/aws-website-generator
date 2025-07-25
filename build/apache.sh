#!/bin/bash
# Update the package index
apt-get update -y

# Install Apache
apt-get install -y apache2

# Enable and start Apache service
systemctl enable apache2
systemctl start apache2

# Optional: replace default web page
# echo "<h1>Hello from your Ubuntu Apache server on AWS!</h1>" > /var/www/html/index.html
