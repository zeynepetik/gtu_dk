import requests
from bs4 import BeautifulSoup

def get_scholar_profile_by_url(profile_url):
    try:
        # Profil URL'sine GET isteği gönder
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.178 Safari/537.36"
        }
        response = requests.get(profile_url, headers=headers)
        response.raise_for_status()

        # Sayfanın HTML içeriğini parse et
        soup = BeautifulSoup(response.text, 'html.parser')

        # Yazarın adını çek
        author_name = soup.find("div", id="gsc_prf_in").text

        # Yazarın açıklamasını çek
        author_affiliation = soup.find("div", class_="gsc_prf_il").text

        # Alıntı sayısını çek
        citation_count = soup.find_all("td", class_="gsc_rsb_std")[0].text

        # Yayınları çek
        publications = []
        for row in soup.find_all("tr", class_="gsc_a_tr"):
            title = row.find("a", class_="gsc_a_at").text
            citation = row.find("td", class_="gsc_a_c").text
            publications.append((title, citation))

        # Bilgileri yazdır
        print(f"Ad: {author_name}")
        print(f"Affiliation: {author_affiliation}")
        print(f"Toplam Alıntı Sayısı: {citation_count}")
        print("\nYayınlar:")
        for pub in publications[:10]:  # İlk 5 yayını göster
            print(f"- {pub[0]} ({pub[1]} alıntı)")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Kullanım
profile_url = input("Google Scholar profil bağlantısını girin: ")
get_scholar_profile_by_url(profile_url)
