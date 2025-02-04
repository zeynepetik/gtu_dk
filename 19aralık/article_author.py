import requests
from bs4 import BeautifulSoup

# Function to search an article title on Google Scholar and fetch authors' emails
def fetch_authors_emails(article_title):
    search_url = f"https://scholar.google.com/scholar?q={'+'.join(article_title.split())}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print(f"Error: Unable to fetch data for article '{article_title}'")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('div', class_='gs_ri')

    for article in articles:
        title_element = article.find('h3', class_='gs_rt')
        if title_element and article_title.lower() in title_element.text.lower():
            authors = article.find('div', class_='gs_a')
            if authors:
                return authors.text

    return "No authors found."

# List of article titles
article_titles = [
    "Novel production strategy of drug-encapsulated biodegradable scaffolds for remediation of hidradenitis suppurativa",
    "Extracts of Cistus creticus cultivated at different salinity levels exhibit promising therapeutic potential for pancreatic cancer cell lines"
]

# Fetch and print authors for each article
def main():
    for title in article_titles:
        print(f"Searching for authors of article: {title}")
        authors = fetch_authors_emails(title)
        if authors:
            print(f"Authors for '{title}': {authors}\n")
        else:
            print(f"No authors found for '{title}'\n")

if __name__ == "__main__":
    main()
