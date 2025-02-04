import requests
from bs4 import BeautifulSoup
import time

# Google Scholar profil bağlantılarının listesi
google_scholar_profiles = [
    "https://scholar.google.com/citations?user=1qKw6SIAAAAJ&hl=tr&oi=ao",
    "https://scholar.google.com/citations?user=SvK0gDEAAAAJ&hl=tr&oi=ao"
]

# Semantic Scholar'da arama yapacak URL
SEMANTIC_SEARCH_URL = "https://www.semanticscholar.org/search"

# Google Scholar profilinden isim alma fonksiyonu
def get_author_name_from_google_scholar(profile_url):
    try:
        response = requests.get(profile_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Yazarın ismini çekmek için doğru etiketi seçiyoruz
        author_name = soup.find("div", id="gsc_prf_in").text.strip()
        return author_name
    except Exception as e:
        print(f"Google Scholar'dan isim çekilemedi: {e}")
        return None

# Semantic Scholar'da yazar arama fonksiyonu
def search_author_in_semantic_scholar(author_name):
    try:
        params = {"q": author_name, "sort": "relevance"}
        response = requests.get(SEMANTIC_SEARCH_URL, params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Semantic Scholar'da yazar sonuçlarını buluyoruz
        authors = []
        for result in soup.find_all("div", class_="result-page-author"):
            name = result.find("a", class_="author-name").text.strip()
            link = result.find("a", class_="author-name")["href"]
            author_id = link.split("/")[-1]
            authors.append({"name": name, "id": author_id, "link": f"https://www.semanticscholar.org{link}"})
        return authors
    except Exception as e:
        print(f"Semantic Scholar'da arama yapılamadı: {e}")
        return []

# Ana işlem
def main():
    for profile in google_scholar_profiles:
        print(f"\nProfil işleniyor: {profile}")
        author_name = get_author_name_from_google_scholar(profile)

        if author_name:
            print(f"Google Scholar'dan alınan isim: {author_name}")
            authors = search_author_in_semantic_scholar(author_name)

            if authors:
                print(f"{author_name} için eşleşmeler:")
                for author in authors:
                    print(f"Ad: {author['name']}, ID: {author['id']}, Link: {author['link']}")
            else:
                print(f"{author_name} için Semantic Scholar'da eşleşme bulunamadı.")
        else:
            print("Google Scholar profilinden isim alınamadı.")
        time.sleep(45)  # Web sitesi bloklanmaması için kısa bir bekleme

if __name__ == "__main__":
    main()
