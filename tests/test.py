from OCRUSREX.ocrusrex import OCRPDF
import os, PyPDF2, tika
tika.initVM()
from tika import parser
import Levenshtein

### TEST SETTINGS
remove_test_output = True #If you want the test OCRed docs to be preserved for some reason, change this to False

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
source_file = os.path.join(dirname, "test.pdf")

#get the benchmark text to compare outputs against
benchmark_text = open(os.path.join(dirname, "full_text.txt")).read()

print("---Testing string source, byte obj return---")
file_obj = OCRPDF(source=source_file)
target_file = os.path.join(dirname, "rawrjr.pdf")
with open(target_file, "wb+") as f:
    f.write(file_obj)
print("\t Levenshtein Distance (~Accuracy): {0}".format(Levenshtein.ratio(extractPdfText(target_file), benchmark_text)*100))
if remove_test_output:
	os.remove(target_file)

print("---Testing string source, string target---")
target_file=os.path.join(dirname, 'lilrawr.pdf')
OCRPDF(source=source_file, targetPath=target_file)
print("\t Levenshtein Distance (~Accuracy): {0}".format(Levenshtein.ratio(extractPdfText(target_file), benchmark_text)*100))
if remove_test_output:
	os.remove(target_file)

print("---Testing byte obj source, byte obj return---")
target_file=os.path.join(dirname, "tinyrawr.pdf")
with open(source_file,'rb') as s:
	file_obj = OCRPDF(source=s.read())
	with open(target_file, "wb+") as f:
		f.write(file_obj)
print("\t Levenshtein Distance (~Accuracy): {0}".format(Levenshtein.ratio(extractPdfText(target_file), benchmark_text)*100))
if remove_test_output:
	os.remove(target_file)

### Switch to test of OCRing of arbitrary page #. Load benchmark text for target page=2
benchmark_text = open(os.path.join(dirname, "page2_text.txt")).read()

print("---Testing byte obj source, byte obj return, and page=2---")
target_file=os.path.join(dirname, "tinyrawr.pdf")
with open(source_file,'rb') as s:
	file_obj = OCRPDF(source=s.read(), page=2)
	with open(target_file, "wb+") as f:
		f.write(file_obj)
print("\t Levenshtein Distance (~Accuracy): {0}".format(Levenshtein.ratio(extractPdfText(target_file), benchmark_text)*100))
if remove_test_output:
	os.remove(target_file)

print("---Testing string source, byte obj return, and page=2---")
file_obj = OCRPDF(source=source_file, page=2)
target_file = os.path.join(dirname, "rawrjr.pdf")
with open(target_file, "wb+") as f:
    f.write(file_obj)
print("\tLevenshtein Distance (~Accuracy): {0}".format(Levenshtein.ratio(extractPdfText(target_file), benchmark_text)*100))
if remove_test_output:
	os.remove(target_file)

print("---Testing string source, string target, and page=2---")
target_file=os.path.join(dirname, 'lilrawr.pdf')
OCRPDF(source=source_file, targetPath=target_file, page=2)
print("\t Levenshtein Distance (~Accuracy): {0}".format(Levenshtein.ratio(extractPdfText(target_file), benchmark_text)*100))
if remove_test_output:
	os.remove(target_file)