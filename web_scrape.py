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

        # UI setup
        self.setup_ui()

        self.session_text = ""

    def setup_ui(self):
        self.setup_scrollbar()
        self.setup_text_display()
        self.setup_buttons()
        self.setup_url_entry()

    def setup_scrollbar(self):
        self.scrollbar = tk.Scrollbar(self.master, width=20)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def setup_text_display(self):
        self.text_display = tk.Text(self.master, wrap="word", height=50, width=120, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_display.yview)
        self.text_display.pack(side=tk.LEFT, pady=10)

    def setup_buttons(self):
        self.start_web_scrape_button = tk.Button(self.master, text="Start Web scrape", command=self.start_web_scrape)
        self.start_web_scrape_button.pack(pady=5)
        self.delete_button = tk.Button(self.master, text="Delete URL", command=self.delete_url)
        self.delete_button.pack(pady=5)
        self.clear_display_button = tk.Button(self.master, text="Clear Display", command=self.clear_display)
        self.clear_display_button.pack(pady=5)

    def setup_url_entry(self):
        self.url_entry = tk.Entry(self.master, width=40)
        self.url_entry.pack(pady=5)

    def start_web_scrape(self):
        url = self.url_entry.get().strip()
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text_to_scrape = self.extract_article_text(soup)

                if text_to_scrape:
                    self.session_text += text_to_scrape
                    self.display_method(text_to_scrape)
                else:
                    self.display_method('No article content found on the webpage')
            else:
                self.display_method('Failed to retrieve webpage content')
        except requests.exceptions.RequestException as e:
            self.display_method(f"Error: {str(e)}")

    def extract_article_text(self, soup):
        article = soup.find('article')
        if article:
            text_content = article.get_text(separator='\n')
            return text_content.strip()
        else:
            return None

    def display_method(self, scraped_text):
        self.text_display.insert(tk.END, scraped_text + "\n")

    def delete_url(self):
        self.url_entry.delete(0, tk.END)

    def clear_display(self):
        self.text_display.delete('1.0', tk.END)    

if __name__ == "__main__":
    root = tk.Tk()
    app = WebScrapingApp(root)
    root.mainloop()