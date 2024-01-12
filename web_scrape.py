import tkinter as tk
import requests
from bs4 import BeautifulSoup

class WebScrapingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Web Scraper")

        # window
        self.master.geometry("1200x800")
        self.master.resizable(False, False)

        # UI 
        self.scrollbar = tk.Scrollbar(self.master, width=20)
        self.text_display = tk.Text(self.master, wrap="word", height=50, width=120, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_display.yview)
        self.start_web_scrape_button = tk.Button(self.master, text="Start Web scrape", command=self.start_web_scrape)
        self.url_entry = tk.Entry(self.master, width=40)
        self.delete_button = tk.Button(self.master, text="Delete URL", command=self.delete_url)

        # UI 
        self.url_entry.pack(pady=5)
        self.start_web_scrape_button.pack(pady=5)
        self.delete_button.pack(pady=5)
        self.text_display.pack(side=tk.LEFT, pady=10)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        
        self.session_text = ""

    def start_web_scrape(self):
        url = self.url_entry.get().strip()
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'}
        response = requests.get(url, headers=headers)

        # rest of the method...

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_to_scrape = self.extract_medium_article_text(soup)

            if text_to_scrape:
                self.session_text += text_to_scrape
                self.new_method(text_to_scrape)
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

    def new_method(self, scraped_text):
        self.text_display.insert(tk.END, scraped_text + "\n")

    def delete_url(self):
        self.url_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = WebScrapingApp(root)
    root.mainloop()