import pandas as pd

# Dosya adı
file_name = "final_isveren.xlsx"  # Kontrol edilecek Excel dosyasının adı

# Dosyayı okuma
df = pd.read_excel(file_name)

# Kopyaları kontrol etme
# Burada hem 'email' hem de 'adisoyadi' sütunlarına göre kopyaları kontrol ediyoruz
duplicates = df[df.duplicated(subset=["email", "adisoyadi"], keep=False)]

# Kopyaları kaydetme
output_file = "kopyalar.xlsx"
duplicates.to_excel(output_file, index=False)

# Sonuç
if not duplicates.empty:
    print(f"Kopyalar bulundu ve '{output_file}' dosyasına kaydedildi.")
else:
    print("Hiçbir kopya bulunamadı.")
