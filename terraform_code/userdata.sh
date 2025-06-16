#!/bin/bash

# #web server install
# sudo yum install -y httpd
# sudop sysmctl enable http --now

# #firewall iadjustment
# sudo firewall-cmd --add-service=http --permanent
# sudo firewall-cmd --reload

# #Using meta data to get instance info
# AZ=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)

# # What will show on the web page
# echo "<h1> Hello from Apache on AL2 </h1>" | sudo tee /var/www/html/index.html
# echo "<p> This Instance is running in AZ: $AZ</p>" | sudo tee -a /var/www/html/index.html

# # turn it off and back on. Always
# sudo systemctl restart httpd




#!/bin/bash

# Update system packages
apt update -y
apt upgrade -y

# Install Apache, PHP, MariaDB (and PHP modules WordPress needs)
apt install -y apache2 php libapache2-mod-php php-mysql php-gd php-xml php-mbstring php-curl php-zip mariadb-server curl unzip

# Enable and start services
systemctl enable apache2 --now
systemctl enable mariadb --now

# Secure MariaDB
mysql -e "UPDATE mysql.user SET authentication_string=PASSWORD('RootStrongPass123!') WHERE User='root';"
mysql -e "DELETE FROM mysql.user WHERE User='';"
mysql -e "DROP DATABASE IF EXISTS test;"
mysql -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"
mysql -e "FLUSH PRIVILEGES;"

# Create WordPress DB and user
DBNAME="wordpress_db"
DBUSER="wp_user"
DBPASS="WpUserStrongPass123!"

mysql -uroot -pRootStrongPass123! -e "CREATE DATABASE ${DBNAME} DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;"
mysql -uroot -pRootStrongPass123! -e "CREATE USER '${DBUSER}'@'localhost' IDENTIFIED BY '${DBPASS}';"
mysql -uroot -pRootStrongPass123! -e "GRANT ALL PRIVILEGES ON ${DBNAME}.* TO '${DBUSER}'@'localhost';"
mysql -uroot -pRootStrongPass123! -e "FLUSH PRIVILEGES;"

# Download WordPress
cd /var/www/html
curl -O https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz
cp -r wordpress/* .
rm -rf wordpress latest.tar.gz

# Set permissions
chown -R www-data:www-data /var/www/html
find /var/www/html -type d -exec chmod 755 {} \;
find /var/www/html -type f -exec chmod 644 {} \;

# Create wp-config.php
cp wp-config-sample.php wp-config.php
sed -i "s/database_name_here/${DBNAME}/" wp-config.php
sed -i "s/username_here/${DBUSER}/" wp-config.php
sed -i "s/password_here/${DBPASS}/" wp-config.php

# Restart Apache
systemctl restart apache2
