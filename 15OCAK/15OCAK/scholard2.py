from scholarly import scholarly
from datetime import datetime, timedelta

def fetch_recent_articles_from_author(scholar_url):
    print(f"Google Scholar URL'si: {scholar_url}")
    try:
        # Google Scholar user ID'yi URL'den ayıklama
        user_id = scholar_url.split("user=")[1].split("&")[0]
        search_query = scholarly.search_author_id(user_id)
        profile = scholarly.fill(search_query)

        # Profil verisini kontrol etmek için yazdır
        print("Profil Verisi:")
        print(profile)

        articles = []
        one_month_ago = datetime.now() - timedelta(days=30)

        for publication in profile.get("publications", []):
            # Yayın verisini kontrol etmek için yazdır
            print("Yayın Verisi:")
            print(publication)

            # Yayın detaylarını işleme
            bib_info = publication.get("bib", {})
            publication_date = bib_info.get("pub_year", None)
            publication_date_full = bib_info.get("pub_date", None)

            # Yayın tarihi kontrolü
            if publication_date_full:
                try:
                    publication_date_full = datetime.strptime(publication_date_full, "%Y-%m-%d")
                except ValueError:
                    publication_date_full = None

            # Yayın bilgilerini saklama
            if publication_date_full and publication_date_full >= one_month_ago:
                articles.append({
                    "title": bib_info.get("title", "Bilinmeyen Başlık"),
                    "url": publication.get("pub_url", "Yok"),
                    "date": publication_date_full.strftime("%Y-%m-%d"),
                    "authors": bib_info.get("author", "Bilinmeyen Yazar"),
                    "venue": bib_info.get("venue", "Bilinmeyen Yayın Yeri"),
                    "abstract": bib_info.get("abstract", "Özet yok"),
                })
            elif publication_date and int(publication_date) >= one_month_ago.year:
                articles.append({
                    "title": bib_info.get("title", "Bilinmeyen Başlık"),
                    "url": publication.get("pub_url", "Yok"),
                    "date": str(publication_date),
                    "authors": bib_info.get("author", "Bilinmeyen Yazar"),
                    "venue": bib_info.get("venue", "Bilinmeyen Yayın Yeri"),
                    "abstract": bib_info.get("abstract", "Özet yok"),
                })

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
        print(f"{i+1}. Başlık: {article['title']}")
        print(f"Yayın Tarihi: {article['date']}")
        print(f"Yazarlar: {article['authors']}")
        print(f"Yayın Yeri: {article['venue']}")
        print(f"Özet: {article['abstract']}")
        print(f"Bağlantı: {article['url']}")
        print("-" * 50)

if __name__ == "__main__":
    main()
