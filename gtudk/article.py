from scholarly import scholarly
import requests
from bs4 import BeautifulSoup

def fetch_articles_from_author(scholar_url):
    print(f"Google Scholar URL'si: {scholar_url}")
    # Profil kullanıcı ID'sini çıkar
    try:
        user_id = scholar_url.split("user=")[1].split("&")[0]
        search_query = scholarly.search_author_id(user_id)
        profile = scholarly.fill(search_query)
        
        articles = []
        for publication in profile.get("publications", []):
            articles.append({
                "title": publication.get("bib", {}).get("title", "Bilinmeyen Başlık"),
                "url": publication.get("pub_url", None)  # Makale bağlantısı
            })
        
        print(f"{len(articles)} makale bulundu.")
        return articles
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return []

def fetch_emails_from_pdf(pdf_url):
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        with open("temp.pdf", "wb") as f:
            f.write(response.content)
        
        # PDF'i okuyup e-posta ayıklama
        import PyPDF2
        emails = set()
        with open("temp.pdf", "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text = page.extract_text()
                emails.update(set(part for part in text.split() if "@" in part and "." in part))
        
        return list(emails)
    except Exception as e:
        print(f"PDF'den e-posta çekme hatası: {e}")
        return []

def main():
    scholar_url = input("Yazarın Google Scholar profil bağlantısını girin: ")
    articles = fetch_articles_from_author(scholar_url)
    
    if not articles:
        print("Hiç makale bulunamadı.")
        return
    
    print("\nMakaleler ve bağlantıları:")
    for i, article in enumerate(articles):
        print(f"{i+1}. {article['title']}")
        print(f"Bağlantı: {article['url'] if article['url'] else 'Yok'}")
        print("-" * 50)

    # Kullanıcıdan PDF linki iste
    pdf_url = input("\nBir makalenin tam metin PDF bağlantısını girin (e-posta ayıklamak için): ")
    if pdf_url:
        emails = fetch_emails_from_pdf(pdf_url)
        print("\nBulunan e-posta adresleri:")
        for email in emails:
            print(email)
    else:
        print("E-posta adresi çıkarılmadı.")

if __name__ == "__main__":
    main()
