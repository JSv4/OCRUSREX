#Copyright 2020 by John Scrudato
#Special thanks to @Abdou from https://stackoverflow.com/questions/47801564/is-it-possible-to-input-pdf-bytes-straight-into-pypdf2-instead-of-making-a-pdf-f
#Special thanks to @Emile Bergeron from https://stackoverflow.com/questions/22795091/how-to-appeand-pdf-pages-using-pypdf2
#Thanks very much for the guidance from http://www.blog.pythonlibrary.org/2013/07/16/pypdf-how-to-write-a-pdf-to-memory/
#Some good (and largely unused

import io, PyPDF2, pytesseract, tempfile, os

from pdf2image import convert_from_path, convert_from_bytes

def OCRPDF(source="", targetPath=None, page=None, nice=5, verbose=False, tesseract_config='--oem 1 --psm 6 -l best/eng -c preserve_interword_spaces=1'):

    try:

        output = PyPDF2.PdfFileWriter()
        page_image_array = []

        #if this is a string..
        if isinstance(source, str):

            if verbose: print("You passed a string in as source. Trying this as source pdf file path.")

            filename, file_extension = os.path.splitext(source)

            if (file_extension == ".pdf"):
                if verbose: print("OCRUSREX - Extracting Images from: {0}".format(source))
                page_image_array = convert_from_path(source)
            else:
                if verbose: print("ERROR - sourcePath must be a file-like object with type "
                     "pdf or must be a pdf with extension .pdf. Found: {0}".format(source))
                return None

        # IF source isn't a string, assume it's a file-like object. If incorrect, error handling will catch this.
        else:
            if verbose: print("OCRUSREX - Try extracting Images from file-like object")
            page_image_array = convert_from_bytes(source)

        if verbose: print("OCRUSREX - Image extraction complete. Starting Tesseract 4.")

        #if a page number was provided, just process that page
        if page:
            if verbose: print("OCRUSREX - You specified a value of {0} for Page. If this is an integer,"
                                " will extract only page with index = page. Otherwise, OCRUSREX will fail.".format(page))
            output.addPage(PyPDF2.PdfFileReader(io.BytesIO(pytesseract.image_to_pdf_or_hocr(page_image_array[page], extension='pdf', nice=nice, config=tesseract_config))).getPage(0))

        #Otherwise process the entire document
        else:
            for (count, image) in enumerate(page_image_array):
                if verbose: print("\tTrying to OCR page {0}".format(count))
                ocred_page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf', nice=nice, config=tesseract_config)

                if verbose: print("\tAdd page {0} to final pdf".format(count))
                output.addPage(PyPDF2.PdfFileReader(io.BytesIO(ocred_page)).getPage(0))

        if verbose: print("OCRUSREX - Successfully processed!")

        #If targetPath was provided, assume that it's a string and valid path. Try to write.
        if targetPath:
            outputStream = open(targetPath, "wb")
            output.write(outputStream)
            outputStream.close()
            # upon success, return truthy values (in this case, True)
            return True

        #otherwise, return results as bytes obj
        else:
            output_file_obj = io.BytesIO()
            output.write(output_file_obj)
            return output_file_obj.getvalue()

    except Exception as e:
        print("ERROR - Exception: {0}".format(e))
        return None

def OCRPDF_tobytesobj(sourcePath="", page=None):

    try:
        if os.path.exists(sourcePath):

            filename, file_extension = os.path.splitext(sourcePath)

            if (file_extension==".pdf"):

                output = PyPDF2.PdfFileWriter()

                print("OCRUSREX - Extracting Images from: {0}".format(sourcePath))
                page_image_array = convert_from_path('/home/jman/test_file.pdf')
                print("OCRUSREX - Image extraction complete. Starting Tesseract 4.")

                for (count, image) in enumerate(page_image_array):

                    print("\tTrying to OCR page {0}".format(count))
                    ocred_page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')

                    print("\tConvert page {0} to pdf and append".format(count))
                    output.addPage(PyPDF2.PdfFileReader(io.BytesIO(ocred_page)).getPage(0))

                    print("\tSuccess!\n")

                output_file_obj = io.BytesIO()
                output.write(output_file_obj)

                return output_file_obj.getvalue()

            else:
                print("ERROR - sourcePath must be a file-like object with type "
                      "pdf or must be a pdf with extension .pdf. Found: {0}".format(sourcePath))
        else:
            print("ERROR - Source path does not exist: {0}".format(sourcePath))

    except Exception as e:
        print("ERROR - Unexpected error: {0}".format(e))
        return None


