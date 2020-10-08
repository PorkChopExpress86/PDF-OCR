import os
import platform

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