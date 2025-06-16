#!/bin/bash

# Update system
sudo apt update -y
sudo apt upgrade -y

# Install dependencies
sudo apt install -y apache2 php libapache2-mod-php php-mysql php-gd php-xml php-mbstring php-curl php-zip mariadb-server curl unzip

# Enable + start services
sudo systemctl enable apache2 --now
sudo systemctl enable mariadb --now

# Secure MariaDB (non-interactive)
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'RootStrongPass123';"
sudo mysql -uroot -pRootStrongPass123 -e "DELETE FROM mysql.user WHERE User='';"
sudo mysql -uroot -pRootStrongPass123 -e "DROP DATABASE IF EXISTS test;"
sudo mysql -uroot -pRootStrongPass123 -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"
sudo mysql -uroot -pRootStrongPass123 -e "FLUSH PRIVILEGES;"

# Create DB + user ## ENV Variables getting SET
DBNAME="wordpress_db"
DBUSER="wp_user"
DBPASS="WpUserStrongPass123"

sudo mysql -uroot -pRootStrongPass123 -e "CREATE DATABASE ${DBNAME} CHARACTER SET utf8 COLLATE utf8_unicode_ci;"
sudo mysql -uroot -pRootStrongPass123 -e "CREATE USER '${DBUSER}'@'localhost' IDENTIFIED BY '${DBPASS}';"
sudo mysql -uroot -pRootStrongPass123 -e "GRANT ALL PRIVILEGES ON ${DBNAME}.* TO '${DBUSER}'@'localhost';"
sudo mysql -uroot -pRootStrongPass123 -e "FLUSH PRIVILEGES;"

# Download + set up WordPress
cd /var/www/html
sudo curl -O https://wordpress.org/latest.tar.gz
sudo tar -xzf latest.tar.gz
sudo cp -r wordpress/* .
sudo rm -rf wordpress latest.tar.gz

# Set permissions
sudo chown -R www-data:www-data /var/www/html
sudo find /var/www/html -type d -exec chmod 755 {} \;
sudo find /var/www/html -type f -exec chmod 644 {} \;

# Configure wp-config.php
sudo cp wp-config-sample.php wp-config.php
sudo sed -i "s/database_name_here/${DBNAME}/" wp-config.php
sudo sed -i "s/username_here/${DBUSER}/" wp-config.php
sudo sed -i "s/password_here/${DBPASS}/" wp-config.php

# Restart Apache
sudo systemctl restart apache2
