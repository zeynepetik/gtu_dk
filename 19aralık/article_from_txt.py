import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_author_info_from_scholar(article_title):
    search_url = f"https://scholar.google.com/scholar?q={'+'.join(article_title.split())}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print(f"Error: Unable to fetch data for article '{article_title}'")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('div', class_='gs_ri')

    for article in articles:
        title_element = article.find('h3', class_='gs_rt')
        if title_element and article_title.lower() in title_element.text.lower():
            authors = article.find('div', class_='gs_a')
            if authors:
                authors_list = authors.text.split(',')
                author_affiliations = []
                for author in authors_list:
                    parts = author.strip().split('-')
                    name = parts[0].strip()
                    affiliation = parts[1].strip() if len(parts) > 1 else "Unknown"
                    author_affiliations.append((name, affiliation))
                return author_affiliations

    return []

def fetch_additional_info_from_web(author_name):
    search_url = f"https://www.google.com/search?q={'+'.join(author_name.split())}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print(f"Error: Unable to fetch data for author '{author_name}'")
        return "Unknown"

    soup = BeautifulSoup(response.text, 'html.parser')
    snippets = soup.find_all('span', class_='st')
    for snippet in snippets:
        if 'university' in snippet.text.lower() or 'institute' in snippet.text.lower():
            return snippet.text

    return "Unknown"

def main():
    # Read article titles from a text file
    input_file = "articles.txt"
    with open(input_file, "r") as file:
        article_titles = [line.strip() for line in file if line.strip()]

    data = []
    for title in article_titles:
        print(f"Searching for authors of article: {title}")
        authors_info = fetch_author_info_from_scholar(title)

        for author, affiliation in authors_info:
            if affiliation == "Unknown":
                affiliation = fetch_additional_info_from_web(author)
            data.append((author, affiliation, title))

    df = pd.DataFrame(data, columns=["Author", "Affiliation", "Article Title"])
    df.to_excel("authors_info.xlsx", index=False)
    print("Excel file 'authors_info.xlsx' has been created.")

if __name__ == "__main__":
    main()
