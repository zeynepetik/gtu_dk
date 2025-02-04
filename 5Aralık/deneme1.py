import pandas as pd
import re

def extract_emails_with_names(file_path, output_file="extracted_emails_with_names.csv"):
    # Load the Excel file into a DataFrame
    try:
        data = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading the file: {e}")
        return
    
    # Check if the required columns exist
    required_columns = ['Author Full Names', 'Email Addresses']
    for col in required_columns:
        if col not in data.columns:
            print(f"The file does not contain a column named '{col}'.")
            return
    
    # Extract email addresses and their corresponding author names
    extracted_data = []
    for _, row in data.iterrows():
        authors = row['Author Full Names']
        emails = row['Email Addresses']
        
        if pd.notna(authors) and pd.notna(emails):
            # Split multiple authors or emails if necessary
            authors_list = [name.strip() for name in str(authors).split(';')]
            emails_list = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', emails)
            
            # Match each email to the author if possible
            for i, email in enumerate(emails_list):
                # If there are more emails than authors, assign "Unknown" to extra emails
                author = authors_list[i] if i < len(authors_list) else "Unknown"
                extracted_data.append({'Author Name': author, 'Email': email})
    
    # Create a DataFrame from the extracted data
    extracted_df = pd.DataFrame(extracted_data)
    
    # Save the extracted data to a CSV file
    extracted_df.to_csv(output_file, index=False)
    print(f"Extracted email addresses with names have been saved to {output_file}.")

# Usage example
# Replace 'your_file.xlsx' with the path to your Excel file
extract_emails_with_names("savedrecs.xlsx")
