# Filteroff Human Features EC2 Instance

## EC2 Instance

g4dn.xlarge

## Installation

```
sudo apt update
sudo apt install -y nginx git software-properties-common python3-pip
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.8

sudo mkdir -p /opt/human-features
sudo chown ubuntu:ubuntu /opt/human-features/
git clone https://github.com/FilterOff/human-features-ec2.git /opt/human-features
cd /opt/human-features
pip install -r requirements.txt

sudo cp /opt/human-features/my_nginx_app /etc/nginx/sites-available/my_nginx_app
sudo ln -s /etc/nginx/sites-available/my_nginx_app /etc/nginx/sites-enabled
sudo systemctl restart nginx

sudo cp /opt/human-features/gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl enable gunicorn.service
sudo systemctl start gunicorn.service

# sudo journalctl -u gunicorn.service

```

# auto stop ec2 instance after 1 hour of running

crontab -e

```
@reboot sleep 3600 && sudo shutdown now
```
