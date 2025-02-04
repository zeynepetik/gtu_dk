import requests
import PyPDF2

def fetch_authors_from_pdf(pdf_url):
    try:
        # PDF dosyasını indirme
        response = requests.get(pdf_url)
        response.raise_for_status()
        with open("temp.pdf", "wb") as f:
            f.write(response.content)

        # PDF'i okuyup yazar bilgilerini ayıklama
        authors = set()
        with open("temp.pdf", "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text = page.extract_text()

                # Yazar bilgilerini ayıklama (örnek: isim arama)
                lines = text.splitlines()
                for line in lines:
                    if any(keyword in line.lower() for keyword in ["author", "yazar", "editor"]):
                        authors.add(line.strip())

        return list(authors)
    except Exception as e:
        print(f"PDF'den yazar bilgisi çekme hatası: {e}")
        return []

def main():
    pdf_url = input("Bir makalenin tam metin PDF bağlantısını girin (yazar ayıklamak için): ")
    if pdf_url:
        authors = fetch_authors_from_pdf(pdf_url)

        print("\nBulunan yazarlar:")
        for author in authors:
            print(author)
    else:
        print("Geçerli bir PDF bağlantısı girilmedi.")

if __name__ == "__main__":
    main()
