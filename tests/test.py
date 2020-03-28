import PyPDF2

from OCRUSREX.ocrusrex import OCRPDF, Multithreaded_OCRPDF
import os, tika, time
tika.initVM()
from tika import parser
import Levenshtein

### TEST SETTINGS
remove_test_output = False #If you want the test OCRed docs to be preserved, change this to False

### HELPER METHODS

# Simple helper method to extract text from resulting pdf using Apache Tika and return the extracted string
# If you want to see the OCRed text in the console, set to echo_ocred_content=True
def extractPdfText(pdfPath, echo_ocred_content = False):

	text = ""
	parsed = parser.from_file(pdfPath)
	text = parsed["content"]
	if echo_ocred_content: print(text)
	return text

### OCRUSREX TESTS

dirname = os.path.dirname(__file__)
source_file = os.path.join(dirname, "test2.pdf")
page_count = PyPDF2.PdfFileReader(source_file).getNumPages()

#get the benchmark text to compare outputs against
benchmark_text = open(os.path.join(dirname, "full_text.txt")).read()

print("\n1) ---Testing string source, byte obj return---")
start = time.time()
file_obj = OCRPDF(source=source_file)
target_file = os.path.join(dirname, "Test1.pdf")
with open(target_file, "wb+") as f:
    f.write(file_obj)
end = time.time()
print("\t Started: {0} | Ended: {1}. ELAPSED: {2} ({3} per page)".format(start, end, end-start, (end-start)/page_count))
print("\t Levenshtein Distance (~Accuracy): {0}".format(Levenshtein.ratio(extractPdfText(target_file), benchmark_text)*100))
if remove_test_output:
	os.remove(target_file)

print("\n2) ---Testing string source, string target---")
start = time.time()
target_file=os.path.join(dirname, 'Test.pdf')
OCRPDF(source=source_file, targetPath=target_file)
end = time.time()
print("\t Started: {0} | Ended: {1}. ELAPSED: {2} ({3} per page)".format(start, end, end-start, (end-start)/page_count))
print("\t Levenshtein Distance (~Accuracy): {0}".format(Levenshtein.ratio(extractPdfText(target_file), benchmark_text)*100))
if remove_test_output:
	os.remove(target_file)

print("\n3) ---Testing byte obj source, byte obj return---")
start = time.time()
target_file=os.path.join(dirname, "Test3.pdf")
with open(source_file,'rb') as s:
	file_obj = OCRPDF(source=s.read())
	with open(target_file, "wb+") as f:
		f.write(file_obj)
end = time.time()
print("\t Started: {0} | Ended: {1}. ELAPSED: {2} ({3} per page)".format(start, end, end-start, (end-start)/page_count))
print("\t Levenshtein Distance (~Accuracy): {0}".format(Levenshtein.ratio(extractPdfText(target_file), benchmark_text)*100))
if remove_test_output:
	os.remove(target_file)

print("\n4) ---MULTITHREAD: Testing string source, byte obj return---")
start = time.time()
file_obj =  Multithreaded_OCRPDF(source=source_file)
target_file = os.path.join(dirname, "Test4.pdf")
with open(target_file, "wb+") as f:
    f.write(file_obj)
end = time.time()
print("\t Started: {0} | Ended: {1}. ELAPSED: {2} ({3} per page)".format(start, end, end-start, (end-start)/page_count))
print("\t Levenshtein Distance (~Accuracy): {0}".format(Levenshtein.ratio(extractPdfText(target_file), benchmark_text)*100))
if remove_test_output:
	os.remove(target_file)

print("\n5) ---MULTITHREAD: Testing string source, string target---")
start = time.time()
target_file=os.path.join(dirname, 'Test5.pdf')
Multithreaded_OCRPDF(source=source_file, targetPath=target_file)
end = time.time()
print("\t Started: {0} | Ended: {1}. ELAPSED: {2} ({3} per page)".format(start, end, end-start, (end-start)/page_count))
print("\t Levenshtein Distance (~Accuracy): {0}".format(Levenshtein.ratio(extractPdfText(target_file), benchmark_text)*100))
if remove_test_output:
	os.remove(target_file)

print("\n6) ---MULTITHREAD: Testing byte obj source, byte obj return---")
start = time.time()
target_file=os.path.join(dirname, "Test6.pdf")
with open(source_file,'rb') as s:
	file_obj = Multithreaded_OCRPDF(source=s.read())
	with open(target_file, "wb+") as f:
		f.write(file_obj)
end = time.time()
print("\t Started: {0} | Ended: {1}. ELAPSED: {2} ({3} per page)".format(start, end, end-start, (end-start)/page_count))
print("\t Levenshtein Distance (~Accuracy): {0}".format(Levenshtein.ratio(extractPdfText(target_file), benchmark_text)*100))
if remove_test_output:
	os.remove(target_file)

### Switch to test of OCRing of arbitrary page #. Load benchmark text for target page=2
benchmark_text = open(os.path.join(dirname, "page2_text.txt")).read()

print("\n7) ---Testing byte obj source, byte obj return, and page=2---")
start = time.time()
target_file=os.path.join(dirname, "Test7.pdf")
with open(source_file,'rb') as s:
	file_obj = OCRPDF(source=s.read(), page=2)
	with open(target_file, "wb+") as f:
		f.write(file_obj)
end = time.time()
print("\t Started: {0} | Ended: {1}. ELAPSED: {2} ({3} per page)".format(start, end, end-start, (end-start)/page_count))
print("\t Levenshtein Distance (~Accuracy): {0}".format(Levenshtein.ratio(extractPdfText(target_file), benchmark_text)*100))
if remove_test_output:
	os.remove(target_file)

print("\n8) ---Testing string source, byte obj return, and page=2---")
start = time.time()
file_obj = OCRPDF(source=source_file, page=2)
target_file = os.path.join(dirname, "Test8.pdf")
with open(target_file, "wb+") as f:
    f.write(file_obj)
end = time.time()
print("\t Started: {0} | Ended: {1}. ELAPSED: {2} ({3} per page)".format(start, end, end-start, (end-start)/page_count))
print("\t Levenshtein Distance (~Accuracy): {0}".format(Levenshtein.ratio(extractPdfText(target_file), benchmark_text)*100))
if remove_test_output:
	os.remove(target_file)

print("\n9) ---Testing string source, string target, and page=2---")
start = time.time()
target_file=os.path.join(dirname, 'Test9.pdf')
OCRPDF(source=source_file, targetPath=target_file, page=2)
end = time.time()
print("\t Started: {0} | Ended: {1}. ELAPSED: {2} ({3} per page)".format(start, end, end-start, (end-start)/page_count))
print("\t Levenshtein Distance (~Accuracy): {0}".format(Levenshtein.ratio(extractPdfText(target_file), benchmark_text)*100))
if remove_test_output:
	os.remove(target_file)