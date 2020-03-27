### What does it do?

OCRUSREX is a simple, no-frills Python 3 library to take a PDF (either by path or as a file-like object), convert
it to images, run it through Tesseract 4 and return it as a PDF.

### Why Another OCR Library?

There are several excellent packages out there to OCR PDFs in Python, but their licensing can be problematic
for potential use in enterprise applications. Also, many of them had way more features than I needed or wanted.
I just needed something to take a PDF, OCR it and give it back to me, without the overhead and potential licensing
headaches of other options out there.

### Install

`pip install ocrusrex`

In addition to installing the required python dependencies, you'll also need tesseract v4. You'll also want to install
the appropriate training data. OCRUSREX is configured to use the best LSTM training models. You can change the default
config to use fast or standard. See a description of the different Tesseract models in the Tesseract Docs:

* https://tesseract-ocr.github.io/tessdoc/Data-Files.html#updated-data-files-for-version-400-september-15-2017

### Dependencies

###### PRODUCTION
        
OCRUSREX relies on three core libraries, all with MIT-like
licenses:

1) pytesseract (MIT)
2) PyPDF2 (MIT-like)
3) Pillow (MIT-like)

Obviously you will need to have already installed Tesseract. Please refer to the Tesseract documentation (or pytesseract docs).

###### TESTS

The tests also rely on:

1) python-levenshtein
2) tika-python.

Neither are required for the core library to work.

### Usage

    from OCRUSREX import ocrusrex
    ocrusrex.OCRPDF(...options)

_RETURNS_: fasly if the task fails or truthy if it succeeds.

_OPTIONS_:

* **source** = ""
  * What is the target PDF to be OCRed? This can be a String containing a valid path to a pdf or a file-like
object.

* **targetPath** = None
  * Where should the OCRed PDF be saved? If you don't provide a value, the odf will be returned as a byte
    object.
  
* **page** = None
  * If you provide an integer value, only a single page will be OCRed and returned. If you leave this as None
            The entire PDF will be OCRed.

* **nice** = 5
   * Sets the priority of the thread in Unix-like operating systems. 5 is slightly elevated.

* **verbose** = False
   * If this is set to True, show messages in the console.

* **tesseract_config** = '--oem 1 --psm 6 -l best/eng -c preserve_interword_spaces=1'
   * This will be passed to pytesseract as the config option. These are the command line arguments
            you would pass directly to tesseract were you calling it directly. The defaults here are
            optimized for accuracy but require you download an additional tesseract data file (the "best" one).
            This comes at the expense of speed.

### FUTURE

This could be multithreaded, potentially, or, as it splits the PDF up first and then OCRs every page separately,
it could esaily be scaled horizontally, particularly if you use the OCRPDF_page_tobytesobj object call.

The use-case I have in mind will be deployed on an asychronous, cloud-based framework. I plan to split my OCR jobs
into multiple calls, each with a single page, and run each one in its own Celery task-runner, so multithreading
directly inside of OCRUSREX isn't a required feature for me. I can see why it would be very helpful for local usage,
however, so, if you know Python multithreading, please feel free to contribute!
