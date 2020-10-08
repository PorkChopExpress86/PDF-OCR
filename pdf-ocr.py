from pdf2image import convert_from_path
import os
import platform
import numpy as np
import cv2
from PIL import Image
import pytesseract

# Detect the os type
os_platform = platform.system()


class PdfToJpg():

    def __init__(self, pdf_path, jpg_path, output_path):

        self.pdf_path = pdf_path
        self.jpg_path = jpg_path
        self.output_path = output_path
    
    
    def convert_pdf_folder_to_jpg_folder(self):
          
        for root, dir_name, file_name in os.walk(self.pdf_source):
            for name in file_name:

                output_file_name = name.replace(".pdf", "")
                
                print(f"Converting: {name}...")
          
                convert_from_path(pdf_path=os.path.join(root, name), output_folder=self.jpg_path, single_file=True, 
                            fmt='jpeg', output_file=output_file_name, grayscale=True, jpegopt={   
                                "quality": 100,
                                "progressive": True,
                                "optimize": True
                            })


    def ocr_jpg_back_to_pdf(self):

        for root, dir_name, file_names in os.walk(self.jpg_path):
            for name in file_names:
                
                # read image into open cv
                image_path = os.path.join(root, name)
                image = cv2.imread(image_path)
                
                # convert image to grayscale
                gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                
                print(f"Writing {name}...")
                
                cv2.imwrite(os.path.join(root,name), gray)
                
                # set tesseract parameters, --psm 11 converts text the best, but format is lost in txt file
                ocr_config = '-l eng --psm 11 --oem 3 -c preserve_interword_spaces=1'

                ## PDF File Conversion: converts a pdf into a readable (searchable) pdf
                text_file_name = "/" + name.replace(".jpg",".txt")
                hocr_file_name = "/" + name.replace(".jpg",".pdf")
                hocr = pytesseract.image_to_pdf_or_hocr(Image.open(os.path.join(root,name)), config=ocr_config)

                with open(self.output_path + hocr_file_name, "w+b") as f:
                    f.write(hocr)



current_path = os.getcwd()
pdf_path = current_path + "/pdf"
jpg_path = current_path + "/jpg"
output_path = current_path + "/output"

convert = PdfToJpg(pdf_path, jpg_path, output_path )
convert.convert_pdf_folder_to_jpg_folder()
convert.ocr_jpg_back_to_pdf()
