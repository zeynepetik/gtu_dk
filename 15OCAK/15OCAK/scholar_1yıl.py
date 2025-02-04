from scholarly import scholarly
from datetime import datetime, timedelta

def fetch_recent_articles_from_profile(profile_url):
    try:
        print(f"Profil URL'si: {profile_url} için son bir yılda yayınlanan makaleler getiriliyor...")
        
        # Yazarın kullanıcı kimliğini URL'den çıkar
        user_id = profile_url.split("user=")[1].split("&")[0]
        
        # Yazar profilini arama
        search_query = scholarly.search_author_id(user_id)
        author = scholarly.fill(search_query)
        
        if not author:
            print("Yazar profili bulunamadı.")
            return
        
        # Son bir yıl için tarih aralığını belirle
        one_year_ago = datetime.now() - timedelta(days=365)
        
        # Makale bilgilerini al
        recent_articles = []
        for publication in author.get("publications", []):
            scholarly.fill(publication)  # Makale detaylarını doldur
            
            # Makale bilgilerini al
            title = publication.get("bib", {}).get("title", "Başlık Bulunamadı")
            year = publication.get("bib", {}).get("pub_year", None)
            journal = publication.get("bib", {}).get("journal", "Dergi Bilgisi Yok")
            citations = publication.get("num_citations", "0")
            authors = publication.get("bib", {}).get("author", "Yazar Bilgisi Yok")
            
            # Yayın yılını kontrol et
            if year:
                try:
                    # Sadece yıl bilgisi varsa, yılın son bir yıl içinde olup olmadığını kontrol et
                    publication_date = datetime(int(year), 1, 1)
                except ValueError:
                    publication_date = None
                
                # Son bir yıl içindeki makaleleri filtrele
                if publication_date and publication_date >= one_year_ago:
                    recent_articles.append({
                        "title": title,
                        "year": year,
                        "citations": citations,
                        "journal": journal,
                        "authors": authors
                    })

        print(f"{len(recent_articles)} son bir yılda yayınlanan makale bulundu.")
        return recent_articles

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return []

def main():
    profile_url = "https://scholar.google.com/citations?hl=tr&user=SvK0gDEAAAAJ&view_op=list_works&sortby=pubdate"
    articles = fetch_recent_articles_from_profile(profile_url)
    
    if not articles:
        print("Son bir yılda yayınlanan makale bulunamadı.")
        return
    
    print("\nSon bir yılda yayınlanan makale bilgileri:")
    for i, article in enumerate(articles):
        print(f"{i+1}. Başlık: {article['title']}")
        print(f"Yıl: {article['year']}")
        print(f"Alıntılanma Sayısı: {article['citations']}")
        print(f"Dergi: {article['journal']}")
        print(f"Yazarlar: {article['authors']}")
        print("-" * 50)

if __name__ == "__main__":
    main()
