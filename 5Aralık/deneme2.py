import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# Excel dosyasını yükleme
input_file = "Kitap3.xlsx"  # Değiştir: Kullanacağınız Excel dosyasının adı
output_file = "emails1.xlsx"  # Çıktı dosyası
data = pd.read_excel(input_file)

# E-posta adreslerini aramak için fonksiyon
def find_email_via_google(author, affiliation, article_title):
    """
    Google üzerinden yazarın e-posta adresini arar.
    """
    search_query = f"{author} {affiliation} {article_title} email"
    url = f"https://www.google.com/search?q={search_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Arama sonuçlarından e-posta adreslerini çıkar
        emails = set()
        for link in soup.find_all("a", href=True):
            if "mailto:" in link["href"]:
                email = link["href"].split("mailto:")[1]
                emails.add(email)
        
        return ", ".join(emails) if emails else "Not Found"
    except Exception as e:
        return f"Error: {str(e)}"

# Ana script
results = []
for index, row in data.iterrows():
    author = row.get("Author Full Names", "")
    affiliation = row.get("Affiliations", "")
    article_title = row.get("Article Title", "")
    
    print(f"Processing: {author}, {affiliation}, {article_title}")
    email = find_email_via_google(author, affiliation, article_title)
    results.append(email)
    
    # Google arama sınırlarına karşı yavaşlatma
    time.sleep(5)  # Her aramada 5 saniye bekle

# E-posta adreslerini orijinal tabloya ekleme
data["Email Addresses"] = results

# Çıktıyı kaydetme
data.to_excel(output_file, index=False)
print(f"E-posta adresleri {output_file} dosyasına kaydedildi.")
