import requests
import time
from datetime import datetime
import pandas as pd

# Yazar ID'si
author_id = "2369727"

# Mevcut yıl ve son iki yıl
current_year = datetime.now().year
last_two_years = {current_year, current_year - 1}

# Yazarın makalelerini listelemek için API URL'si
author_url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers?fields=title,year,authors,paperId"

response = requests.get(author_url)

if response.status_code == 200:
    data = response.json()
    articles = data.get("data", [])

    # Makale bilgilerini saklamak için liste
    articles_data = []

    if articles:
        for article in articles:
            year = article.get("year")

            # Yıl kontrolü
            if year and int(year) in last_two_years:
                title = article.get("title", "Bilinmeyen Başlık") or "Bilinmeyen Başlık"
                authors = ", ".join([author["name"] for author in article.get("authors", [])]) if article.get("authors") else "Yazar Bilgisi Yok"
                paper_id = article.get("paperId", "ID Yok") or "ID Yok"

                # Makale detayları için API URL'si
                detail_url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields=title,abstract,authors,year,venue,citationCount,referenceCount"
                detail_response = requests.get(detail_url)

                if detail_response.status_code == 200:
                    paper_details = detail_response.json()
                    articles_data.append({
                        "Başlık": paper_details.get("title", "Bilgi yok"),
                        "Özet": paper_details.get("abstract", "Özet yok"),
                        "Yıl": paper_details.get("year", "Yıl yok"),
                        "Yayın Yeri": paper_details.get("venue", "Yayın yeri yok"),
                        "Alıntı Sayısı": paper_details.get("citationCount", "Bilinmiyor"),
                        "Referans Sayısı": paper_details.get("referenceCount", "Bilinmiyor"),
                        "Yazarlar": ", ".join([author.get("name", "Bilinmeyen Yazar") for author in paper_details.get("authors", [])])
                    })
                else:
                    print(f"Makale detaylarına erişim başarısız oldu: {detail_response.status_code}")

                # Her istekten sonra bekleme süresi
                time.sleep(60)  # 1 saniye bekle

        # Verileri Excel dosyasına kaydet
        if articles_data:
            df = pd.DataFrame(articles_data)
            excel_file = "makale_bilgi.xlsx"
            df.to_excel(excel_file, index=False, engine='openpyxl')
            print(f"Makale bilgileri '{excel_file}' dosyasına kaydedildi.")
        else:
            print("Kaydedilecek makale bulunamadı.")
    else:
        print("Yazara ait makale bulunamadı.")
else:
    print(f"Yazarın makalelerine erişim başarısız oldu: {response.status_code}")
