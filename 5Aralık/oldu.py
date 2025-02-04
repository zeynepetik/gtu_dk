import pandas as pd
import re

def extract_emails_from_excel(file_path, output_file="extracted_emails.csv"):
    # Load the Excel file into a DataFrame
    try:
        data = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading the file: {e}")
        return
    
    # Check if the column "Email Addresses" exists
    if 'Email Addresses' not in data.columns:
        print("The file does not contain a column named 'Email Addresses'.")
        return
    
    # Extract email addresses
    data['Email Addresses'] = data['Email Addresses'].astype(str)  # Ensure all entries are strings
    email_addresses = data['Email Addresses'].str.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    
    # Flatten the list of lists and remove duplicates
    email_list = [email for sublist in email_addresses for email in sublist]
    unique_emails = list(set(email_list))
    
    # Save the extracted emails to a CSV file
    pd.DataFrame(unique_emails, columns=['Email']).to_csv(output_file, index=False)
    print(f"Extracted email addresses have been saved to {output_file}.")

# Usage example
# Replace 'your_file.xlsx' with the path to your Excel file
extract_emails_from_excel("savedrecs.xlsx")
