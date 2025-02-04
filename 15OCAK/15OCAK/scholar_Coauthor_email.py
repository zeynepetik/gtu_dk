import requests
from bs4 import BeautifulSoup

def get_scholar_profile_and_coauthors(profile_url):
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

        # Yazarın açıklamasını çek (örneğin: üniversite veya kurum bilgisi)
        author_affiliation = soup.find("div", class_="gsc_prf_il").text

        # E-posta bilgisini çek
        email_info = soup.find("div", class_="gsc_prf_ivh").text if soup.find("div", class_="gsc_prf_ivh") else "E-posta bilgisi yok"

        # Katkıda bulunan yazarları ve bağlantılarını çek
        co_authors_section = soup.find_all("a", class_="gsc_rsb_aa")
        co_authors = [
            {
                "name": co_author.text,
                "profile_url": f"https://scholar.google.com{co_author['href']}"
            }
            for co_author in co_authors_section
        ]

        # Ana yazar bilgileri
        print(f"Ad: {author_name}")
        print(f"Açıklama: {author_affiliation}")
        print(f"E-posta: {email_info}")
        print("\nKatkıda Bulunan Yazarlar ve E-posta Bilgileri:")

        # Katkıda bulunan yazarların profillerini dolaş ve bilgilerini al
        for co_author in co_authors:
            print(f"\n- İsim: {co_author['name']}")
            print(f"  Profil URL: {co_author['profile_url']}")

            try:
                # Katkıda bulunan yazarın profil sayfasına git
                co_author_response = requests.get(co_author['profile_url'], headers=headers)
                co_author_response.raise_for_status()
                co_author_soup = BeautifulSoup(co_author_response.text, 'html.parser')

                # E-posta bilgisini çek
                co_author_email = co_author_soup.find("div", class_="gsc_prf_ivh").text if co_author_soup.find("div", class_="gsc_prf_ivh") else "E-posta bilgisi yok"
                print(f"  E-posta: {co_author_email}")

            except Exception as e:
                print(f"  Bilgi alınamadı: {e}")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Kullanım
profile_url = 'https://scholar.google.com/citations?user=1qKw6SIAAAAJ&hl=tr&oi=ao'
get_scholar_profile_and_coauthors(profile_url)
