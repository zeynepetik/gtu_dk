import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def search_researchgate_with_proxy(article_title):
    search_url = f"https://www.researchgate.net/search?q={article_title.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    proxies = {
        "http": "http://your_proxy:port",
        "https": "https://your_proxy:port"
    }
    try:
        response = requests.get(search_url, headers=headers, proxies=proxies, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        emails = set()
        for a in soup.find_all('a', href=True):
            if "mailto:" in a["href"]:
                emails.add(a["href"].split(":")[1])
        
        text_emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', soup.text))
        emails.update(text_emails)

        return list(emails)
    except Exception as e:
        print(f"Error fetching data for article: {article_title}: {e}")
        return []


# Bir makale başlığı için yazar e-postalarını bulma
if __name__ == "__main__":
    article_title = input("Enter the article title: ")
    print(f"Searching for emails related to the article: {article_title}")
    
    emails = search_researchgate_with_proxy(article_title)
    
    if emails:
        print(f"Found the following emails for the article '{article_title}':")
        for email in emails:
            print(email)
    else:
        print(f"No emails found for the article '{article_title}'.")
