import time
import requests

# İlk olarak, bir yazarın makalelerini almak için API isteği yapıyoruz
author_id = "2369727"
url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers?fields=title,year,authors,paperId"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    articles = data.get("data", [])
    
    if articles:
        for i, article in enumerate(articles[:5]):  # İlk 5 makaleyi alalım
            paper_id = article.get("paperId")
            print(f"\nSeçilen Makale ID: {paper_id}")
            
            # Detaylar için API isteği
            detail_url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields=title,abstract,authors,year,venue,citationCount,referenceCount"
            detail_response = requests.get(detail_url)
            
            if detail_response.status_code == 200:
                paper_details = detail_response.json()
                print("Makale Detayları:")
                print(f"Başlık: {paper_details.get('title', 'Bilgi yok')}")
                print(f"Özet: {paper_details.get('abstract', 'Özet yok')}")
                print(f"Yıl: {paper_details.get('year', 'Yıl yok')}")
                print(f"Yayın Yeri: {paper_details.get('venue', 'Yayın yeri yok')}")
                print(f"Alıntı Sayısı: {paper_details.get('citationCount', 'Bilinmiyor')}")
                print(f"Referans Sayısı: {paper_details.get('referenceCount', 'Bilinmiyor')}")
            else:
                print(f"Makale detaylarına erişim başarısız oldu: {detail_response.status_code}")
            
            # Her istekten sonra bekleme süresi
            time.sleep(60)  # 1 saniye bekle
    else:
        print("Yazara ait makale bulunamadı.")
else:
    print(f"Yazarın makalelerine erişim başarısız oldu: {response.status_code}")
