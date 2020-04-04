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
the appropriate training data. OCRUSREX is configured to use the "best" english LSTM training dataset. You can change this
config to use fast or standard quality by overriding the tesseract_config argument. Using best improves accuracy by about 
1 - 3 percentage points based on my benchmarking with a performance hit of ~ 20% more time per page. On a VirtualBox dev
environment, that meant going from 2 seconds to 2.38 seconds per page when using byte obj input and out (string paths are
much slower). I was willing to take that tradeoff as I hate having re-OCR things, but your mileage may vary.

If you want to use tesseract's "best" training sets, you will likely need to install it for your 
system. See a description of the different Tesseract models in the Tesseract Docs:

* https://tesseract-ocr.github.io/tessdoc/Data-Files.html#updated-data-files-for-version-400-september-15-2017

### Dependencies

###### PRODUCTION
        
OCRUSREX relies on four core libraries, all with MIT-like
licenses:

1) pytesseract (MIT)
2) PyPDF2 (MIT-like)
3) Pillow (MIT-like)
4) uqfoundation/multiprocess (MIT-like)

Obviously you will need to have already installed Tesseract 4. Please refer to the Tesseract documentation (or pytesseract docs).

###### TESTS

The tests also rely on:

1) python-levenshtein
2) tika-python.

Neither are required for the core library to work.

### Usage

###### Single Threaded

    from OCRUSREX import ocrusrex
    ocrusrex.OCRPDF(source="", targetPath=None, page=None, nice=5, verbose=False, tesseract_config='--oem 1 -l eng -c preserve_interword_spaces=1 textonly_pdf=1')

_RETURNS_: fasly if the task fails or truthy if it succeeds. If you specify a targetPath, returns True to indicate success
or false to indicate failure. If you don't specify a targetPath, returns a bytes obj on success or None on failure. 

###### Multi Threaded

OCRUSREX supports multithreaded execution via the core Python 3 multithreading library. Based on intial testing, this 
execution mode enables you to divide OCR time per page vs singlethreaded by the number of threads you specify.
For example, assuming you have the requisite # of cores, running threads=4 will divide ocr time per page by 4, effectively
reducing OCR time by 75%. Multithreading performance is almost identical to running seperate processes. This is likely due
to OCRUSREX always calling separate instances of tesseract, so it's effectively callings separate processes whether you choose
multithreaded or multiprocessed execution.

    from OCRUSREX import ocrusrex
    ocrusrex.Multithreaded_OCRPDF(source="", targetPath=None, processes=4, nice=5, verbose=False, tesseract_config='--oem 1 -l eng -c preserve_interword_spaces=1 textonly_pdf=1')

_RETURNS_: fasly if the task fails or truthy if it succeeds. If you specify a targetPath, returns True to indicate success
or false to indicate failure. If you don't specify a targetPath, returns a bytes obj on success or None on failure. 

###### Multi Processed

OCRUSREX supports multiprocessed execution via the uqfoundation/multiprocess library. Based on intial testing, this 
execution mode enables you to divide OCR time per page vs singlethreaded by the number of processes you specify.
For example, assuming you have the requisite # of cores, running processes=4 will divide ocr time per page by 4, effectively
reducing OCR time by 75%. This method may be removed in the future as it appears to offer no real performance advantages
over using multithreading, yet it comes at the expense of an additional dependency.

    from OCRUSREX import ocrusrex
    ocrusrex.Multiprocessed_OCRPDF(source="", targetPath=None, threads=4, nice=5, verbose=False, tesseract_config='--oem 1 -l eng -c preserve_interword_spaces=1 textonly_pdf=1')

_RETURNS_: fasly if the task fails or truthy if it succeeds. If you specify a targetPath, returns True to indicate success
or false to indicate failure. If you don't specify a targetPath, returns a bytes obj on success or None on failure. 

##### OPTIONS:

* **processes** = 4 [**_Multiprocessed Only_**]
  * How many processes should be spawned at one time? Default is 4. Initial guidance is this should not be > your # of effective cores. 

* **threads** = 4 [**_Multithreaded Only_**]
  * How many threads should be used at once. Default is 4. Because the threads spawn new tesseract instances, the multithreaded performance is quite similiar to multiprocessed.

* **source** = ""
  * What is the target PDF to be OCRed? This can be a String containing a valid path to a pdf or a file-like
object.

* **targetPath** = None
  * Where should the OCRed PDF be saved? If you don't provide a value, the pdf will be returned as a byte
    object.
  
* **page** = None [**_Singlethreaded Only_**]
  * If you provide an integer value, only a single page will be OCRed and returned. If you leave this as None
            the entire PDF will be OCRed. **PDF page starting index # is 1 NOT 0**.

* **nice** = 5
   * Sets the priority of the thread in Unix-like operating systems. 5 is slightly elevated.

* **verbose** = False
   * If this is set to True, show messages in the console.

* **tesseract_config** = '--oem 1 --psm 6 -l best/eng -c preserve_interword_spaces=1'
   * This will be passed to pytesseract as the config option. These are the command line arguments
            you would pass directly to tesseract were you calling it directly. The defaults here are
            optimized for accuracy but require you download an additional tesseract data file (the "best" one).
            This comes at the expense of speed.

* **tesseract_config** = 'print'
   * Pass a method in for this argument to have verbose OCR message passed to this function as the first argument. 
   If you leave it as None, standard print() function is used.

* **logger** = None
   * If you want to pass a specific logger in to expose inner verbose messages (particularly for multithreaded and multiprocessed versions),
   Pass the logger object in here. It must support .info and .error calls. If you leave this as None, verbose uses standard Python print() function.

### FUTURE

I am pretty happy with the baseline performance at this point. The tool can OCR PDFs at a rate of 1 page every 2 seconds.

The most important next feature is reducing the output file size. Output PDFs are currently substantially larger than the
source files. I need to do some experimentation to see if this can be done AFTER feeding the high-quality images to Tesseract.

After that, it would be good to do some more error checking and other automated cleanup. Other libraries out there have
substantial codebases dedicated just to these kinds of cleanup tasks. For now, I expect I'll add these types of features
organically over time as I discover particularly hairy situations that need to be addressed or where I need some type of output
for myself. Contributions are welcome!