import os
from PyPDF2 import PdfFileWriter, PdfFileReader

inputdir = "/mnt/c/development/Brisbane_POC/All PDF Plans"
outputdir = "/mnt/c/development/Brisbane_POC/All PDF Plans_split"
os.makedirs(outputdir, exist_ok=True)
for dirpath, dirnames, filenames in os.walk(inputdir):
    for file in filenames:
        if file.endswith(".pdf"):
            print(file)
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