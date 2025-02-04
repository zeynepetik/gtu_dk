import pandas as pd

# Excel dosyalarının adları
file1 = "sümeyye_akademik.xlsx"  # İlk dosya
file2 = "eslesenakademik.xlsx"  # İkinci dosya

# Dosyaları yükleme
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

# İkinci dosyadaki email sütunlarını bir listeye çevirme
emails_to_remove = df2['email'].tolist()

# İlk dosyadan bu email adreslerini çıkarma
df1_cleaned = df1[~df1['email'].isin(emails_to_remove)]

# Temizlenmiş dosyayı kaydetme
output_file = "ayrılmısakademik.xlsx"
df1_cleaned.to_excel(output_file, index=False)

print(f"Eşleşen e-posta adresleri temizlendi ve '{output_file}' dosyasına kaydedildi.")
