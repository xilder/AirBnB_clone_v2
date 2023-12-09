#!/usr/bin/env bash
# installs nginx if not already installed and then creates some files in the servers

# install nginx
sudo apt-get update
sudo apt -y install nginx
sudo apt -y install ufw
sudo ufw allow 'Nginx HTTP'

# create foldders and give permissions
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/current/
chown -R ubuntu:ubuntu /data/

PAGE=\
"<!DOCTYPE html>
<html>
	<head>
		xilder
	<\head>
	<body>
		<h1>Hello World!<\h1>
	<\body>
</html>"
sudo echo "$PAGE" > /data/web_static/releases/test/index.html
sudo ln -sf  /data/web_static/releases/test/ /data/web_static/current

ALIAS=\
"server {
	listen 80 default_server;
	listen [::]:80 default_server;

	server_name _;
	index index.html index.htm;
	error_page 404 /404.html;

	location /hbnb_static/ {
		alias /data/web_static/current/;
	}
	location / {
		root /var/www/html/;
		try_files \$uri \$uri/ =404;
	}
}
"
sudo echo "$ALIAS" > /etc/nginx/sites-enabled/default

sudo service nginx restart
