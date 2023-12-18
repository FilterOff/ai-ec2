# Filteroff Human Features EC2 Instance

## EC2 Instance

g4dn.xlarge ubuntu instance

## Installation

```
sudo apt update
sudo apt install -y nginx git software-properties-common python3-pip build-essential dkms ubuntu-drivers-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.8

# install nvidia drivers
sudo ubuntu-drivers autoinstall

# verify nvidia drivers
nvidia-smi

git clone https://github.com/FilterOff/ai-ec2.git /opt
sudo chown ubuntu:ubuntu /opt/human-features/
sudo chown ubuntu:ubuntu /opt/chubby/
pip install -r /opt/human-features/requirements.txt
pip install -r /opt/chubby/requirements.txt

sudo mv /opt/my_nginx_app /etc/nginx/sites-available/my_nginx_app
sudo ln -s /etc/nginx/sites-available/my_nginx_app /etc/nginx/sites-enabled
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx

sudo mv /opt/humanfeatures.service /etc/systemd/system/humanfeatures.service
sudo systemctl enable humanfeatures.service
sudo systemctl start humanfeatures.service

sudo mv /opt/chubby.service /etc/systemd/system/chubby.service
sudo systemctl enable chubby.service
sudo systemctl start chubby.service

echo "**************************************************************************"
echo "Make sure you change out os.environ.get('MODEL_URL') in /opt/chubby/app.py"
echo "**************************************************************************"

sudo journalctl -f -u humanfeatures.service

```

# auto stop ec2 instance after 1 hour of running

crontab -e

```
@reboot sleep 3600 && sudo shutdown now
```
