from pyzbar.pyzbar import decode
from PIL import Image
import pdfplumber
import fitz
import re


class PDFReader:

    @staticmethod
    def __get_barcode_data(file_path):

        pdf_document = fitz.open(file_path)

        if pdf_document.page_count < 1:
            raise Exception("Not valid document")

        page = pdf_document.load_page(0)
        pix = page.get_pixmap()
        image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

        barcodes = decode(image)

        barcode_data_list = []
        for barcode in barcodes:
            barcode_data_list.append(barcode.data.decode('utf-8'))

        return barcode_data_list if barcode_data_list else "incomplete data"

    def get_pdf_data(self, file_path):

        pdf_file = pdfplumber.open(file_path)
        file_data_string = ""

        for i in pdf_file.pages:
            file_data_string += i.extract_text().replace("\n", " ")

        """Remove spaces between words and colons"""
        pattern = r'\s:'
        correct_string = re.sub(pattern, ':', file_data_string).replace("TAGGED BY:", "")

        final_dict = {}

        """Find the title and immediately insert the value from scanning the barcode."""
        pattern = r'^(.*?)PN:'
        match_title = re.findall(pattern, correct_string)
        final_dict[match_title[0].rstrip()] = self.__get_barcode_data(file_path)[1]

        """Since the documents are standard, as we'll be checking them for the presence of all elements,
                I'll hardcode the name to save time."""
        final_dict["TAGGED BY"] = self.__get_barcode_data(file_path)[0]

        """"create dictionary"""
        words = correct_string.split()
        for i in range(len(correct_string.split())):
            word = words[i]
            if word.endswith(":"):
                key = word[:-1]
                if i + 1 < len(words) and not words[i + 1].endswith(":"):
                    value = words[i + 1]
                else:
                    value = "value not found!"
                final_dict[key] = value

        pdf_file.close()

        return final_dict
