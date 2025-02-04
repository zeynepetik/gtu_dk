from scholarly import scholarly
from datetime import datetime, timedelta

def fetch_recent_articles_from_profile(profile_url):
    try:
        print(f"Profil URL'si: {profile_url} için son bir ayda yayınlanan makaleler getiriliyor...")
        
        # Yazarın kullanıcı kimliğini URL'den çıkar
        user_id = profile_url.split("user=")[1].split("&")[0]
        
        # Yazar profilini arama
        search_query = scholarly.search_author_id(user_id)
        author = scholarly.fill(search_query)
        
        if not author:
            print("Yazar profili bulunamadı.")
            return
        
        # Son bir ay için tarih aralığını belirle
        one_month_ago = datetime.now() - timedelta(days=30)
        
        # Makale bilgilerini al
        recent_articles = []
        for publication in author.get("publications", []):
            scholarly.fill(publication)  # Makale detaylarını doldur
            
            # Makale bilgilerini al
            title = publication.get("bib", {}).get("title", "Başlık Bulunamadı")
            year = publication.get("bib", {}).get("pub_year", None)
            journal = publication.get("bib", {}).get("journal", "Dergi Bilgisi Yok")
            citations = publication.get("num_citations", "0")
            
            # Yayın yılını kontrol et
            if year:
                try:
                    # Sadece yıl bilgisi varsa, yılın son bir ay içinde olup olmadığını kontrol et
                    publication_date = datetime(int(year), 1, 1)
                except ValueError:
                    publication_date = None
                
                # Son bir ay içindeki makaleleri filtrele
                if publication_date and publication_date >= one_month_ago:
                    recent_articles.append({
                        "title": title,
                        "year": year,
                        "citations": citations,
                        "journal": journal
                    })

        print(f"{len(recent_articles)} son bir ayda yayınlanan makale bulundu.")
        return recent_articles

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return []

def main():
    profile_url = input("Google Scholar profil URL'sini girin (ör. 'https://scholar.google.com/citations?user=XXXXXXXXXX'): ")
    articles = fetch_recent_articles_from_profile(profile_url)
    
    if not articles:
        print("Son bir ayda yayınlanan makale bulunamadı.")
        return
    
    print("\nSon bir ayda yayınlanan makale bilgileri:")
    for i, article in enumerate(articles):
        print(f"{i+1}. Başlık: {article['title']}")
        print(f"Yıl: {article['year']}")
        print(f"Alıntılanma Sayısı: {article['citations']}")
        print(f"Dergi: {article['journal']}")
        print("-" * 50)

if __name__ == "__main__":
    main()