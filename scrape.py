import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pytesseract
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import os

class OCRApp:
    def __init__(self, master):
        self.master = master
        self.master.title("OCR Demo")

        # window
        self.master.geometry("1200x800")
        self.master.resizable(False, False)

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        # UI elements
        self.image_label = tk.Label(self.master)
        self.text_display = tk.Text(self.master, wrap="word", height=10, width=50)
        self.select_image_button = tk.Button(self.master, text="Select Image", command=self.select_image_ocr)
        self.start_web_ocr_button = tk.Button(self.master, text="Start Web scrape", command=self.start_web_ocr)
        self.summary_button = tk.Button(self.master, text="Print", command=self.summarize_session)
        self.url_entry = tk.Entry(self.master, width=40)
        self.delete_button = tk.Button(self.master, text="Delete URL", command=self.delete_url)

        # UI layout
        self.image_label.pack(pady=10)
        self.select_image_button.pack(pady=5)
        self.url_entry.pack(pady=5)
        self.start_web_ocr_button.pack(pady=5)
        self.delete_button.pack(pady=5)
        self.text_display.pack(pady=10)
        self.summary_button.pack(pady=5)

        # Session
        self.session_text = ""

    def select_image_ocr(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.display_image(file_path)
            extracted_text = self.perform_image_ocr(file_path)
            self.session_text += extracted_text
            self.new_method(extracted_text)

    def start_web_ocr(self):
        url = self.url_entry.get().strip()
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_to_ocr = self.extract_medium_article_text(soup)

            if text_to_ocr:
                extracted_text = self.perform_web_ocr(text_to_ocr)
                if extracted_text:
                    self.session_text += extracted_text
                    self.new_method(extracted_text)
                else:
                    print('No text found in the article for OCR')
            else:
                print('No article content found on the webpage')
        else:
            print('Failed to retrieve webpage content')

    def extract_medium_article_text(self, soup):
        article = soup.find('article')
        if article:
            text_content = article.get_text(separator='\n')
            return text_content.strip()
        else:
            return None

    def perform_web_ocr(self, text):
     cleaned_text = unidecode(text) if text else ''

     try:
         extracted_text = pytesseract.image_to_string(cleaned_text, lang='eng')
     except Exception as e:
         print(f"Error during OCR: {e}")
         extracted_text = ""

     return extracted_text

    def perform_image_ocr(self, image_path):
        image = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text

    def new_method(self, extracted_text):
        self.text_display.insert(tk.END, extracted_text + "\n")

    def display_image(self, image_path):
        img = Image.open(image_path)
        img.thumbnail((300, 300))
        img = ImageTk.PhotoImage(img)
        self.image_label.configure(image=img)
        self.image_label.image = img

    def summarize_session(self):
        print("Session Summary:")
        print(self.session_text)

    def delete_url(self):
        self.url_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
