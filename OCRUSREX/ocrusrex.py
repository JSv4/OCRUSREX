#Copyright 2020 by John Scrudato
#Special thanks to @Abdou from https://stackoverflow.com/questions/47801564/is-it-possible-to-input-pdf-bytes-straight-into-pypdf2-instead-of-making-a-pdf-f
#Special thanks to @Emile Bergeron from https://stackoverflow.com/questions/22795091/how-to-appeand-pdf-pages-using-pypdf2
#Thanks very much for the guidance from http://www.blog.pythonlibrary.org/2013/07/16/pypdf-how-to-write-a-pdf-to-memory/

import io, pytesseract, PyPDF2, os, time
from multiprocess import Pool
from pdf2image import convert_from_path, convert_from_bytes

#based on what I've read in several different projects, limiting Tesseract to single threading with this environment variable
#leads to optimal performance. From OCRUSREX, we'll call multiple, single-threaded tesseract instances. I've verified that
#using 4 threads in OCRUSREX is much much faster than lifting the Tesseract thread cap.
os.environ['OMP_THREAD_LIMIT'] = '1'

def ocrPilImage(image=None, nice=5, config=""):
	ocred_page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf', nice=nice, config=config)
	return PyPDF2.PdfFileReader(io.BytesIO(ocred_page)).getPage(0)

#Single-threaded invocation of tesseract. No page range support (yet).
def OCRPDF(source="", targetPath=None, page=None, nice=5, verbose=False, tesseract_config='--oem 1 -l best/eng -c preserve_interword_spaces=1 textonly_pdf=1', logCallback=None):

	try:

		output = PyPDF2.PdfFileWriter()

		#if this is a string..
		if isinstance(source, str):

			if verbose: (logCallback if logCallback else print)("You passed a string in as source. Trying this as source pdf file path.")

			page_count = PyPDF2.PdfFileReader(source).getNumPages()
			filename, file_extension = os.path.splitext(source)

			if (file_extension == ".pdf"):
				if verbose: (logCallback if logCallback else print)("OCRUSREX - Try extracting Images from path: {0}".format(source))

				if page is None:

					if verbose: (logCallback if logCallback else print)("\tOCRing entire document with total page count of: {0}".format(page_count))

					for i in range(0, page_count):
						if verbose: (logCallback if logCallback else print)("\tOCRing page {0} of {1}".format(i+1, page_count))
						page_image_array = convert_from_path(source, dpi=300, first_page=i+1, last_page=i+1)
						pdf_page = ocrPilImage(image=page_image_array[0], nice=nice, config=tesseract_config)
						output.addPage(pdf_page)

				else:

					if verbose: (logCallback if logCallback else print)("\tOCRing only page {0} of {1}".format(page, page_count))

					page_image_array = convert_from_path(source, dpi=300, first_page=page, last_page=page)
					output.addPage(ocrPilImage(image=page_image_array[0], nice=nice, config=tesseract_config))

					if verbose: print("Done")

		# IF source isn't a string, assume it's a file-like object. If incorrect, error handling will catch this.
		else:

			if verbose: (logCallback if logCallback else print)("OCRUSREX - Try extracting Images from bytes object")
			page_count = PyPDF2.PdfFileReader(io.BytesIO(source)).getNumPages()

			if page is None:

				if verbose: print("\tOCRing entire document with total page count of: {0}".format(page_count))

				for i in range(0, page_count):
					if verbose: print("\tOCRing page {0} of {1}".format(i+1, page_count))
					page_image_array = convert_from_bytes(source, dpi=100, first_page=i+1, last_page=i+1)
					output.addPage(ocrPilImage(image=page_image_array[0], nice=nice,
					                           config=tesseract_config))

			else:
				if verbose: (logCallback if logCallback else print)("\tOCRing only page {0} of {1}".format(page, page_count))
				page_image_array = convert_from_bytes(source, dpi=100, first_page=page, last_page=page)
				output.addPage(ocrPilImage(image=page_image_array[0], nice=nice,
				                           config=tesseract_config))

		if verbose: (logCallback if logCallback else print)("OCRUSREX - Successfully processed!")

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
		(logCallback if logCallback else print)("ERROR - Exception: {0}".format(e))
		return None

#Multithreaded execution of Tesseract. This version requires you ocr the entire pdf. No single page or page range support (yet).
def Multithreaded_OCRPDF(source="", targetPath=None, processes=4, nice=5, verbose=False, tesseract_config='--oem 1 -l best/eng -c preserve_interword_spaces=1 textonly_pdf=1', logCallback=None):

	if isinstance(source, str):
		if verbose: (logCallback if logCallback else print)("You passed a string in as source. Trying this as source pdf file path.")
		page_count = PyPDF2.PdfFileReader(source).getNumPages()
	else:
		if verbose: (logCallback if logCallback else print)("OCRUSREX - Try extracting Images from bytes object")
		page_count = PyPDF2.PdfFileReader(io.BytesIO(source)).getNumPages()

	output = PyPDF2.PdfFileWriter()

	# set up a multiprocess pool with the specified number of processes. Then call the single-threaded OCRPDF pethod
	# on each page
	p = Pool(processes)
	for ocred_page in p.map(lambda p: OCRPDF(source=source, verbose=verbose, nice=nice, page=p+1, tesseract_config=tesseract_config, logCallback=logCallback), range(0, page_count)):
		output.addPage(PyPDF2.PdfFileReader(io.BytesIO(ocred_page)).getPage(0))

	if verbose: (logCallback if logCallback else print)("Multithreaded Execution Complete!")

	# If targetPath was provided, assume that it's a string and valid path. Try to write.
	if targetPath:
		outputStream = open(targetPath, "wb")
		output.write(outputStream)
		outputStream.close()
		# upon success, return truthy values (in this case, True)
		return True

	# otherwise, return results as bytes obj
	else:
		output_file_obj = io.BytesIO()
		output.write(output_file_obj)
		return output_file_obj.getvalue()

	if verbose: (logCallback if logCallback else print)("Complete! Elapsed time: {0}".format(end-start))