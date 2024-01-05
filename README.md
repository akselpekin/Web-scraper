# OCR Demo Application

This is a simple Optical Character Recognition (OCR) application built with Python and Tkinter. It uses the Tesseract OCR engine to extract text from images and web pages.

## Features

- Extract text from images
- Extract text from web pages
- Display extracted text in a scrollable text box
- Delete URL from the entry field

## Dependencies

- Python 3
- Tkinter
- Pillow
- pytesseract
- requests
- BeautifulSoup
- unidecode

## Installation

1. Install Python 3 and pip if they are not installed.
2. Clone this repository.
3. Navigate to the cloned repository.
4. Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:

```bash
python scrape.py
```

2. To extract text from an image, click the "Select Image" button and select an image file.
3. To extract text from a web page, enter the URL in the entry field and click the "Start Web scrape" button.
4. The extracted text will be displayed in the text box on the right.
5. To delete the URL from the entry field, click the "Delete URL" button.


