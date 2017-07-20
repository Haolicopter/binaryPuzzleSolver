#!/bin/sh
#=========================================================
echo "Installing tools..."
#=========================================================
sudo apt-get zip

#=========================================================
echo "Download the latest chrome..."
#=========================================================
wget "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo rm google-chrome-stable_current_amd64.deb
sudo apt-get install -y -f

#=========================================================
echo "Download latest selenium server..."
#=========================================================
SELENIUM_VERSION=$(curl "https://selenium-release.storage.googleapis.com/" | perl -n -e'/.*<Key>([^>]+selenium-server-standalone[^<]+)/ && print $1')
wget "https://selenium-release.storage.googleapis.com/${SELENIUM_VERSION}" -O selenium-server-standalone.jar
chown ubuntu:ubuntu selenium-server-standalone.jar

#=========================================================
echo "Download latest chrome driver..."
#=========================================================
CHROMEDRIVER_VERSION=$(curl "http://chromedriver.storage.googleapis.com/LATEST_RELEASE")
wget "http://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
sudo rm chromedriver_linux64.zip
chown ubuntu:ubuntu chromedriver
mv chromedriver /usr/local/bin/

#=========================================================
echo "Installing selenium..."
#=========================================================
pip install selenium