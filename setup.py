import os
import glob


cwd = os.getcwd()

clear_folders = input("Do you want to clear the following folders: pdf, jpg and output? Y/N ")

if clear_folders.lower() == "y":
    folder_paths = ["pdf", "jpg", "output"]
    
    for folders in folder_paths:
        files = glob.glob(cwd + "/" + folders + "/*")
        for f in files:
            os.remove(f)

try:
    os.mkdir("./pdf")
except:
    print("pdf folder already exists...")

try:
    os.mkdir("./jpg")
except:
    print("jpg folder already exists...")

try:
    os.mkdir(".output")
except:
    print("output already exists...")