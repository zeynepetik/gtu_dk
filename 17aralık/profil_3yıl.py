from scholarly import scholarly
from datetime import datetime
import pandas as pd

def has_recent_publications(profile, years=3):
    """ Profili kontrol eder ve son belirtilen yıl içinde yayın varsa True döner. """
    current_year = datetime.now().year
    for pub in profile.get('publications', []):  # Yayınlara eriş
        try:
            year = int(pub.get('bib', {}).get('pub_year', 0))  # Yayın yılı
            if current_year - year <= years:  # Son 3 yıl içinde mi?
                return True
        except ValueError:
            continue  # Yıl değeri düzgün değilse atla
    return False

def search_university_authors(university_name):
    print(f"{university_name} ile ilgili yazarlar aranıyor...")
    search_query = scholarly.search_author(university_name)
    authors = []

    try:
        for author in search_query:  # Tüm sonuçları işle
            try:
                profile = scholarly.fill(author, sections=['publications'])  # Yayın bilgilerini doldur
                if has_recent_publications(profile, years=3):  # Son 3 yılda yayını olanları kontrol et
                    authors.append({
                        "name": profile.get("name"),
                        "scholar_url": f"https://scholar.google.com/citations?user={profile.get('scholar_id')}"
                    })
                    print(f"Yazar bulundu: {profile.get('name')}")
            except Exception as e:
                print(f"Profili işlerken hata oluştu: {e}")
    except Exception as e:
        print(f"Hata oluştu: {e}")
    
    return authors

def save_to_excel(authors, filename="authors_profiles.xlsx"):
    """ Yazar bilgilerini Excel dosyasına kaydeder. """
    if authors:
        df = pd.DataFrame(authors)  # Veriyi pandas DataFrame'e dönüştür
        df.to_excel(filename, index=False, engine='openpyxl')  # Excel dosyasına kaydet
        print(f"Veriler başarıyla '{filename}' dosyasına kaydedildi.")
    else:
        print("Kaydedilecek veri bulunamadı.")

def main():
    university_name = "Gebze Technical University"
    authors = search_university_authors(university_name)

    if authors:
       #print("\nSon 3 yılda yayını olan yazarlar ve bağlantıları:")
        for author in authors:
            print(f"İsim: {author['name']}")
            print(f"Google Scholar Profili: {author['scholar_url']}")
            print("-" * 50)
        
        # Excel'e kaydetme işlemi
        save_to_excel(authors)
    else:
        print("Hiçbir uygun yazar bulunamadı.")

if __name__ == "__main__":
    main()
