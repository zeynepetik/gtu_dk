import pandas as pd

# Excel dosyalarını yükleme
file1 = "final_academic.xlsx"  # İlk dosyanın adı
file2 = "karasız.xlsx"  # İkinci dosyanın adı

# Dosyaları okuma
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

# Eşleşme kontrolü: email ya da adisoyadi sütunları aynı olanlar
matching_rows = df1.merge(df2, on=["email", "adisoyadi"], how="inner")

# Yalnızca email sütunu eşleşen satırları kontrol etme
email_only_match = df1.merge(df2, on="email", how="inner").drop_duplicates()

# İki sonucu birleştirme (hem email hem adisoyadi eşleşenler ve sadece email eşleşenler)
result = pd.concat([matching_rows, email_only_match]).drop_duplicates()

# Sonucu bir Excel dosyasına kaydetme
output_file = "eslesen.xlsx"
result.to_excel(output_file, index=False)

print(f"Eşleşen kayıtlar '{output_file}' dosyasına kaydedildi.")
