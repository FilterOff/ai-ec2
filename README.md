# Filteroff Human Features EC2 Instance

## EC2 Instance

g4dn.xlarge

## Installation

```
sudo apt update
sudo apt install nginx git software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.8

sudo mkdir -p /opt/human-features
git clone https://github.com/FilterOff/human-features-ec2.git /opt/human-features

cp my_nginx_app /etc/nginx/sites-available/my_nginx_app
sudo ln -s /etc/nginx/sites-available/my_nginx_app /etc/nginx/sites-enabled
sudo systemctl restart nginx

cp /opt/human-features/gunicorn.service /etc/systemd/system/gunicorn.service
systemctl enable gunicorn.service
systemctl start gunicorn.service

```

# auto stop ec2 instance after 1 hour of running

crontab -e

```
@reboot sleep 3600 && sudo shutdown now
```
