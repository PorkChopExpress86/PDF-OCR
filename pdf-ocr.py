from pdf2image import convert_from_path
import os
import cv2
from PIL import Image
import pytesseract


class PdfToJpg:
    def __init__(self, pdf_path, jpg_path, output_path):

        self.pdf_path = pdf_path
        self.jpg_path = jpg_path
        self.output_path = output_path

    def convert_pdf_folder_to_jpg_folder(self, fail_list):

        for root, dir_name, file_name in os.walk(self.pdf_path):
            num_of_files = len(os.listdir(root))
            file_count = 0
            for name in file_name:

                output_file_name = name.replace(".pdf", ".jpg")

                if os.path.exists(os.path.join(self.jpg_path, output_file_name)):
                    file_count += 1
                    percent_done = round((file_count / num_of_files * 100), 1)
                    print(f"{percent_done}% done: {name} already exists, skipping...")
                else:
                    # print(f"Converting: {name} to jpg...")
                    try:
                        convert_from_path(
                            pdf_path=os.path.join(root, name),
                            output_folder=self.jpg_path,
                            single_file=True,
                            fmt="jpeg",
                            output_file=name.replace(".pdf", ""),
                            grayscale=True,
                            jpegopt={
                                "quality": 100,
                                "progressive": True,
                                "optimize": True,
                            },
                        )
                        file_count += 1
                        percent_done = round((file_count / num_of_files * 100), 1)
                        print(f"{percent_done}% done: {output_file_name} converted...")
                    except:
                        print(f"Could not convert {name}")
                        fail_list.append(name)

    def ocr_jpg_back_to_pdf(self, fail_list):

        for root, dir_name, file_names in os.walk(self.jpg_path):
            num_of_files = len(os.listdir(root))
            file_count = 0
            for name in file_names:

                new_pdf_name = name.replace(".jpg", ".pdf")
                if os.path.exists(os.path.join(self.output_path, new_pdf_name)):
                    file_count += 1
                    percent_done = round((file_count / num_of_files * 100), 1)
                    print(
                        f"{percent_done}% done: {new_pdf_name} already exists, skipping..."
                    )
                else:
                    # read image into open cv
                    image_path = os.path.join(root, name)
                    image = cv2.imread(image_path)

                    # convert image to grayscale
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                    cv2.imwrite(os.path.join(root, name), gray)

                    # set tesseract parameters, --psm 11 converts text the best, but format is lost in txt file
                    ocr_config = (
                        "-l eng --psm 11 --oem 3 -c preserve_interword_spaces=1"
                    )

                    try:
                        ## PDF File Conversion: converts a pdf into a readable (searchable) pdf
                        hocr_file_name = "/" + name.replace(".jpg", ".pdf")
                        hocr = pytesseract.image_to_pdf_or_hocr(
                            Image.open(os.path.join(root, name)), config=ocr_config
                        )

                        with open(self.output_path + hocr_file_name, "w+b") as f:
                            f.write(hocr)
                        file_count += 1
                        percent_done = round((file_count / num_of_files * 100), 1)
                        print(f"{percent_done}%: {new_pdf_name} is a searchable pdf...")
                    except:
                        file_name = name.replace(".jpg", ".pdf")
                        print(f"Failure to convert {name}...")
                        fail_list.append(file_name)


def main():
    current_path = os.getcwd()
    pdf_path = current_path + "/pdf"
    jpg_path = current_path + "/jpg"
    output_path = current_path + "/output"

    to_jpg_fail_list = []
    to_pdf_fail_list = []

    convert = PdfToJpg(pdf_path, jpg_path, output_path)
    convert.convert_pdf_folder_to_jpg_folder(to_jpg_fail_list)
    convert.ocr_jpg_back_to_pdf(to_pdf_fail_list)

    if len(to_jpg_fail_list) > 0:
        print(
            f"The following pdfs were not converted into jpgs: {str(to_jpg_fail_list)}"
        )

    if len(to_pdf_fail_list) > 0:
        print(
            f"The following pdfs were not converted into jpgs: {str(to_pdf_fail_list)}"
        )


if __name__ == "__main__":
    main()
