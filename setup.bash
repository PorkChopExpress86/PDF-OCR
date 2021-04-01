#!/bin/bash

echo "Installing dependencies..."
sudo apt install build-essential python3.9-venv poppler-utils tesseract-ocr-eng python3-tesserocr -y

echo "Createing python virtual environment..."
python3.9 -m venv venv
. ./venv/bin/activate

echo "Installing python packages"
python -m pip install --upgrade pip setuptools
python -m pip install -r requirements.txt

# Setup folder structure
