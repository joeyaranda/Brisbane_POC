import os
import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader
import fire
import fitz
import collections


class PDFSplitter(object):

    def check_duplicate(self,inputallplansdir):

        list_all_pdf = []
        a=0
        for dirpath, dirnames, filenames in os.walk(inputallplansdir):
            for file in filenames:
                if file.endswith(".pdf"):
                    a+=1
                    print(a,file)
                    list_all_pdf.append(file)
        
        check_list_all_pdf = ([item for item, count in collections.Counter(list_all_pdf).items() if count > 1])
        print(check_list_all_pdf)


    def split_pdf(self,inputdir,outputdir):

        # inputdir = "/mnt/c/development/Brisbane_POC/Test"
        # outputdir = "/mnt/c/development/Brisbane_POC/Test_split"
        a=0
        os.makedirs(outputdir, exist_ok=True)
        for dirpath, dirnames, filenames in os.walk(inputdir):
            for file in filenames:
                if file.endswith(".pdf"):
                    a+=1
                    print(a,file)
                    filename = os.path.join(dirpath,file)
                    inputpdf = PdfFileReader(open(filename, "rb"),strict=False)

                    for i in range(inputpdf.numPages):
                        output = PdfFileWriter()
                        output.addPage(inputpdf.getPage(i))
                        split_filename = ((file.split("."))[0]).replace(" ","")
                        folder_origin = ((dirpath.split("/"))[-1]).replace(" ","")
                        concat_folder_filename = folder_origin+"_"+split_filename
                        with open(outputdir+ "/" +f"{concat_folder_filename}_%02d.pdf" % (i+1), "wb") as outputStream:
                            output.write(outputStream)

    def split_pdf_to_image(self,inputsplitdir,outputimagedir,mode,dpi_val):
        # file_path = "my_file.pdf"

        os.makedirs(outputimagedir,exist_ok=True)
        for dirpath, dirnames, filenames in os.walk(inputsplitdir):
            for file in filenames:

                if mode == "default" and dpi_val == "Null":
                    file_path = os.path.join(dirpath,file)
                    doc = fitz.open(file_path)  # open document
                    for page in doc:
                        pix = page.get_pixmap()  # render page to an image
                        name = (file.split("."))[0]
                        print(name)
                        pix.save(outputimagedir+"/"+f"{name}.png")
                elif mode == "high-res":
                    file_path = os.path.join(dirpath,file)
                    dpi = dpi_val
                    zoom = dpi/72
                    magnify = fitz.Matrix(zoom,zoom)
                    doc = fitz.open(file_path)  # open document
                    for page in doc:
                        pix = page.get_pixmap(matrix=magnify)  # render page to an image
                        name = (file.split("."))[0]
                        print(name)
                        pix.save(outputimagedir+"/"+f"{name}.png")


if __name__ == "__main__":
    fire.Fire(PDFSplitter)