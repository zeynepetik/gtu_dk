import requests

# API'den veriyi çek
url = "https://api.semanticscholar.org/graph/v1/author/2369727/papers?fields=title,year,authors,paperId"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    articles = data.get("data", [])

    # Başlık satırı
    print(f"{'Başlık':<80} {'Yıl':<5} {'Yazarlar':<50} {'Makale ID':<40}")
    print("-" * 180)
    
    for article in articles:
        # Verileri kontrol ederek al
        title = article.get("title", "Bilinmeyen Başlık") or "Bilinmeyen Başlık"
        year = str(article.get("year", "Yıl Yok")) or "Yıl Yok"
        authors = ", ".join([author["name"] for author in article.get("authors", [])]) if article.get("authors") else "Yazar Bilgisi Yok"
        paper_id = article.get("paperId", "ID Yok") or "ID Yok"
        
        # Formatlama ve yazdırma
        print(f"{title:<80} {year:<5} {authors:<50} {paper_id:<40}")
else:
    print(f"API isteği başarısız oldu: {response.status_code}")
