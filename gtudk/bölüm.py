from scholarly import scholarly
import openpyxl

def search_university_authors(university_name, department_name=None, max_results=50):
    print(f"{university_name} üniversitesindeki {department_name or 'tüm bölümler'} ile ilgili yazarlar aranıyor...")
    search_query = scholarly.search_author(university_name)
    authors = []

    try:
        # İlk `max_results` kadar sonucu işliyoruz
        for i, author in enumerate(search_query):
            if i >= max_results:
                break  # Belirtilen sayıda sonuçtan sonra döngüyü kır
            try:
                profile = scholarly.fill(author)  # Profili doldur
                affiliation = profile.get("affiliation", "Bilinmiyor")
                
                # Bölüm filtrelemesi yap
                if department_name and department_name.lower() not in affiliation.lower():
                    continue
                
                authors.append({
                    "name": profile.get("name"),
                    "affiliation": affiliation,
                    "scholar_url": f"https://scholar.google.com/citations?user={profile.get('scholar_id')}"
                })
                print(f"Yazar bulundu: {profile.get('name')} ({affiliation})")
            except Exception as e:
                print(f"Profili işlerken hata oluştu: {e}")
    except Exception as e:
        print(f"Hata oluştu: {e}")

    return authors

def save_to_excel(authors, filename="authors.xlsx"):
    # Yeni bir Excel dosyası oluştur
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Authors"

    # Başlık satırını ekle
    sheet.append(["İsim", "Bağlı Olduğu Üniversite/Kuruluş", "Google Scholar Profili"])

    # Yazar bilgilerini ekle
    for author in authors:
        sheet.append([author["name"], author["affiliation"], author["scholar_url"]])

    # Excel dosyasını kaydet
    workbook.save(filename)
    print(f"Sonuçlar {filename} dosyasına kaydedildi.")

def main():
    university_name = input("Üniversite adı girin: ")
    department_name = input("Bölüm adı girin (tüm bölümler için boş bırakın): ")
    max_results = int(input("Kaç sonuç getirilmesini istersiniz? (Varsayılan: 50): ") or 50)

    authors = search_university_authors(university_name, department_name, max_results)

    if authors:
        print("\nBulunan yazarlar:")
        for author in authors:
            print(f"İsim: {author['name']}")
            print(f"Bağlı Olduğu Üniversite/Kuruluş: {author['affiliation']}")
            print(f"Google Scholar Profili: {author['scholar_url']}")
            print("-" * 50)

        save_to_excel(authors, f"{university_name.replace(' ', '_')}_authors.xlsx")
    else:
        print("Hiçbir yazar bulunamadı.")

if __name__ == "__main__":
    main()
