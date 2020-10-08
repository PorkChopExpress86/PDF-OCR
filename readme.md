# PDF OCR

This is made to run on ubuntu or wsl2 in windows with python3.8

Install all linux dependencies first with the following command, (requires sudo):

- sudo apt install build-essential python3-pip python3-venv poppler-utils tesseract-ocr-eng python3-tesserocr -y

Create python venv called env-ocr:
- python3 -m venv env-ocr

Activate environment:
- source ./env-ocr/bin/activate

Install python dependencies with pip:
- pip install pdf2image opencv-python notebook numpy pillow pytesseract

Once everything is installed run ./setup.py to create the folders for your files.

Copy the pdfs you want to convert in the pdf folder and run ./pdf-ocr.py