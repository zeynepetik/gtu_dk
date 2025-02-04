import requests
from bs4 import BeautifulSoup

def fetch_html_content(scholar_url):
    """Google Scholar yazar sayfasının HTML içeriğini al."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(scholar_url, headers=headers)
    
    if response.status_code == 200:
        print("HTML içeriği başarıyla alındı.")
        return response.text
    else:
        print(f"HTML içeriği alınamadı. Durum kodu: {response.status_code}")
        return None

def fetch_all_articles(html_content):
    """HTML içeriğinden tüm makale başlıklarını ve bağlantılarını ayıkla."""
    soup = BeautifulSoup(html_content, "html.parser")
    articles = []
    
    # Google Scholar'daki her makale bloğu "gs_ri" sınıfında
    for result in soup.find_all("div", class_="gs_ri"):
        title_tag = result.find("h3", class_="gs_rt")
        
        if title_tag:
            title = title_tag.get_text(strip=True)  # Makale başlığı
            url = title_tag.find("a")["href"] if title_tag.find("a") else None  # Makale bağlantısı
            
            articles.append({
                "title": title,
                "url": url if url else "Bağlantı bulunamadı"
            })
    
    return articles

def main():
    scholar_url = input("Google Scholar yazar profil URL'sini girin: ")
    html_content = fetch_html_content(scholar_url)
    
    if not html_content:
        print("HTML içeriği alınamadı.")
        return
    
    print("Tüm makaleler aranıyor...")
    all_articles = fetch_all_articles(html_content)
    
    if not all_articles:
        print("Hiç makale bulunamadı.")
    else:
        print("\nTüm Makaleler:")
        for i, article in enumerate(all_articles, 1):
            print(f"{i}. {article['title']}")
            print(f"Bağlantı: {article['url']}")
            print("-" * 50)

if __name__ == "__main__":
    main()
