from scholarly import scholarly
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def fetch_recent_articles_from_author(scholar_url):
    print(f"Google Scholar URL'si: {scholar_url}")
    # Profil kullanıcı ID'sini çıkar
    try:
        user_id = scholar_url.split("user=")[1].split("&")[0]
        search_query = scholarly.search_author_id(user_id)
        profile = scholarly.fill(search_query)
        
        articles = []
        one_month_ago = datetime.now() - timedelta(days=30)  # Son bir ay
        
        for publication in profile.get("publications", []):
            publication_date = publication.get("bib", {}).get("pub_year", None)
            publication_date_full = publication.get("bib", {}).get("pub_date", None)
            
            if publication_date_full:
                try:
                    publication_date_full = datetime.strptime(publication_date_full, "%Y-%m-%d")
                except ValueError:
                    publication_date_full = None
            
            if publication_date_full and publication_date_full >= one_month_ago:
                articles.append({
                    "title": publication.get("bib", {}).get("title", "Bilinmeyen Başlık"),
                    "url": publication.get("pub_url", None),  # Makale bağlantısı
                    "date": publication_date_full.strftime("%Y-%m-%d"),
                })
            elif publication_date and int(publication_date) >= one_month_ago.year:
                # Sadece yıl bilgisi varsa
                articles.append({
                    "title": publication.get("bib", {}).get("title", "Bilinmeyen Başlık"),
                    "url": publication.get("pub_url", None),
                    "date": str(publication_date),
                })
        
        print(f"{len(articles)} son bir ayda yayınlanan makale bulundu.")
        return articles
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return []

def main():
    scholar_url = input("Yazarın Google Scholar profil bağlantısını girin: ")
    articles = fetch_recent_articles_from_author(scholar_url)
    
    if not articles:
        print("Son bir ayda yayınlanan makale bulunamadı.")
        return
    
    print("\nSon bir ayda yayınlanan makaleler ve bağlantıları:")
    for i, article in enumerate(articles):
        print(f"{i+1}. {article['title']}")
        print(f"Yayın Tarihi: {article['date']}")
        print(f"Bağlantı: {article['url'] if article['url'] else 'Yok'}")
        print("-" * 50)

if __name__ == "__main__":
    main()
