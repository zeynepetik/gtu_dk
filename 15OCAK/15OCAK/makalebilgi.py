import requests

# Semantic Scholar API'ye istek gönder
url = "https://api.semanticscholar.org/graph/v1/author/2369727/papers?fields=title,year,authors"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    # Veriyi organize etmek ve tablo halinde göstermek
    def format_articles(data):
        articles = data.get("data", [])
        formatted_articles = []
        
        for article in articles:
            title = article.get("title", "Bilinmeyen Başlık")
            year = article.get("year", "Yıl Belirtilmemiş")
            authors = ", ".join([author["name"] for author in article.get("authors", [])])
            paper_id = article.get("paperId", "ID Yok")
            
            formatted_articles.append({
                "Başlık": title,
                "Yıl": year,
                "Yazarlar": authors,
                "Makale ID": paper_id
            })
        
        return formatted_articles

    # Veriyi organize et ve kullanıcıya göster
    articles = format_articles(data)

    # Tabloyu bastır
    print(f"{'Başlık':<80} {'Yıl':<5} {'Yazarlar':<50} {'Makale ID':<40}")
    print("-" * 180)
    for article in articles:
        print(f"{article['Başlık']:<80} {article['Yıl']:<5} {article['Yazarlar']:<50} {article['Makale ID']:<40}")
else:
    print(f"İstek başarısız oldu: {response.status_code}")
