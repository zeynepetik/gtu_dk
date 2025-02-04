import openai
import pandas as pd

# OpenAI API anahtarınızı buraya ekleyin
openai.api_key = "gtu_dk"

def ask_openai(question):
    """
    OpenAI API'ye soru sorar ve yanıtı döndürür.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Kullanmak istediğiniz model (örneğin, gpt-4)
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def process_excel(input_path, output_path):
    """
    Excel dosyasındaki satırları işler ve OpenAI API'si ile her satır için yanıt alır.
    """
    # Excel dosyasını yükleyin
    df = pd.read_excel(input_path)

    # Yanıtlar için yeni bir sütun ekleyin
    df['OpenAI_Response'] = ""

    # Her satır için API'yi çağır
    for index, row in df.iterrows():
        # Satır verilerini birleştirerek soruyu oluştur
        row_data = " ".join(str(cell) for cell in row if pd.notna(cell))
        question = f"Give me the affiliations and contact address of all the authors of this paper: {row_data}"
        
        print(f"Processing row {index + 1}/{len(df)}...")
        response = ask_openai(question)
        df.at[index, 'OpenAI_Response'] = response

    # Sonuçları yeni bir Excel dosyasına kaydedin
    df.to_excel(output_path, index=False)
    print(f"Results saved to {output_path}")

# Kullanım
input_file = "savedrecs.xlsx"  # Girdi dosyanızın yolu
output_file = "output.xlsx"  # Çıktı dosyasının yolu

process_excel(input_file, output_file)
