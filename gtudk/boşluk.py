import pandas as pd

# Excel dosyasını yükleyin
file_path = 'your_excel_file.xlsx'
output_file = 'empty_rows.xlsx'  # Boşluk olanları kaydedeceğiniz dosyanın adı

# Veri çerçevesini yükleyin
df = pd.read_excel(file_path)

# Kontrol etmek istediğiniz sütunu belirtin (örneğin 'email' sütunu)
empty_rows = df[df['email'].isna()]  # Boş değerleri seçer

# Boşluk olanları bir dosyaya kaydet
if not empty_rows.empty:
    empty_rows.to_excel(output_file, index=False)
    print(f"{len(empty_rows)} adet boş değer bulundu. 'empty_rows.xlsx' dosyasına kaydedildi.")
else:
    print("Sütunda boşluk yok.")
