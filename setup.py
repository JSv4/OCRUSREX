import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OCRUSREX",
    version="0.1.0",
    author="John Scrudato",
    author_email="john@thelegal.engineer",
    description="OCRUSREX takes a PDF (either by path or as a file-like object) and makes it searchable using Tesseract 4. It has an enterprise-friendly license.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JSv4/OCRUSREX",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pillow', 'pypdf2', 'pdf2image','pytesseract','python-Levenshtein', 'tika']
)