#!/bin/bash

termux-setup-storage

pkg install termux-api

echo "checking working of termux api"

termux-sms-list - 1

echo 'installing git'

pkg install git

echo 'installing python and dependencies'

pkg install python && pip install bs4 && pip install requests


touch token.txt
