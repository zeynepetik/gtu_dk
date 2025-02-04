from scholarly import scholarly
import pandas as pd


def search_university_authors(university_name, max_results=10):
    print(f"{university_name} ile ilgili yazarlar aranıyor...")
    search_query = scholarly.search_author(university_name)
    authors = []
    
    try:
        # İlk `max_results` kadar sonucu işliyoruz
        for i, author in enumerate(search_query):
            if i >= max_results:
                break  # Belirtilen sayıda sonuçtan sonra döngüyü kır
            try:
                profile = scholarly.fill(author)  # Profili doldur
                authors.append({
                    "name": profile.get("name"),
                    "affiliation": profile.get("affiliation", "Bilinmiyor"),
                    "scholar_url": f"https://scholar.google.com/citations?user={profile.get('scholar_id')}"
                })
                print(f"Yazar bulundu: {profile.get('name')} ({profile.get('affiliation')})")
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
        print("\nBulunan yazarlar ve bağlantıları:")
        for author in authors:
            print(f"İsim: {author['name']}")
            print(f"Bağlı Olduğu Üniversite/Kuruluş: {author['affiliation']}")
            print(f"Google Scholar Profili: {author['scholar_url']}")
            print("-" * 50)
        save_to_excel(authors)
    else:
        print("Hiçbir yazar bulunamadı.")

if __name__ == "__main__":
    main()
