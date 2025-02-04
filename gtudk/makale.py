from scholarly import scholarly
import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_articles_and_coauthors(scholar_url):
    """ Bir yazarın makale isimlerini ve bağlantılı diğer yazarları getirir. """
    articles_data = []
    try:
        user_id = scholar_url.split("user=")[1].split("&")[0]
        author_profile = scholarly.search_author_id(user_id)
        profile = scholarly.fill(author_profile, sections=["publications"])
        
        for publication in profile.get("publications", []):
            title = publication.get("bib", {}).get("title", "Bilinmeyen Başlık")
            pub_url = publication.get("pub_url", None)  # Makale URL'sini al
            
            if pub_url:
                linked_authors = fetch_authors_from_url(pub_url)  # Detaylı sayfadan yazarları çek
            else:
                linked_authors = "Yazar bilgisi bulunamadı"
            
            articles_data.append({
                "article_title": title,
                "linked_authors": linked_authors
            })
    except Exception as e:
        print(f"Makale bilgileri çekerken hata oluştu: {e}")
    
    return articles_data

def fetch_authors_from_url(url):
    """ Bir makalenin URL'sinden yazar bilgilerini çeker. """
    print("aaaaaaaaaaaaaaaaaaaaa")
    print(f"Tarama yapılacak URL: {url}")

    try:
        print(f"Makale sayfası taranıyor: {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        # Sayfayı BeautifulSoup ile parse et
        soup = BeautifulSoup(response.text, "html.parser")
        authors = []
        
        # Google Scholar sayfasındaki yazar bilgileri genelde 'gsc_oci_value' class'ında bulunur
        for author in soup.find_all("a", class_="gsc_oci_value"):
            authors.append(author.text.strip())
        
        return ", ".join(authors) if authors else "Yazar bilgisi bulunamadı"
    except Exception as e:
        print(f"Sayfadan yazar bilgisi çekerken hata oluştu: {e}")
        return "Yazar bilgisi bulunamadı"

def search_university_authors(university_name, max_results=1):
    """ Üniversiteye bağlı yazarları bulur. """
    print(f"{university_name} ile ilgili yazarlar aranıyor...")
    search_query = scholarly.search_author(university_name)
    authors = []
    
    try:
        for i, author in enumerate(search_query):
            if i >= max_results:
                break
            try:
                profile = scholarly.fill(author)
                authors.append({
                    "name": profile.get("name"),
                    "affiliation": profile.get("affiliation", "Bilinmiyor"),
                    "scholar_url": f"https://scholar.google.com/citations?user={profile.get('scholar_id')}"
                })
                print(f"Yazar bulundu: {profile.get('name')} ({profile.get('affiliation')})")
            except Exception as e:
                print(f"Profili işlerken hata oluştu: {e}")
    except Exception as e:
        print(f"Hata oluştu: {e}")
    
    return authors

def save_articles_to_excel(data, filename="articles_with_coauthors.xlsx"):
    """ Makale isimleri ve yazarları içeren veriyi Excel'e kaydeder. """
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False, engine='openpyxl')
    print(f"Makale verileri başarıyla '{filename}' dosyasına kaydedildi.")

def main():
    university_name = "Gebze Technical University"
    authors = search_university_authors(university_name, max_results=1)
    all_articles = []

    if authors:
        print("\nBulunan yazarlar ve bağlantıları:")
        for author in authors:
            print(f"İsim: {author['name']}")
            print(f"Google Scholar Profili: {author['scholar_url']}")
            print("-" * 50)

            # Yazarların makalelerini ve bağlantılı kişilerini getir
            articles = fetch_articles_and_coauthors("https://scholar.google.com/citations?user=uMbX8AUAAAAJ")
            for article in articles:
                all_articles.append({
                    "author_name": author['name'],
                    "article_title": article['article_title'],
                    "linked_authors": article['linked_authors']
                })
        
        # Makale bilgilerini Excel'e kaydet
        save_articles_to_excel(all_articles)
    else:
        print("Hiçbir yazar bulunamadı.")

if __name__ == "__main__":
    main()
