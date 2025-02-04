import re
import pandas as pd

def extract_emails_from_excel(file_path, email_column=None):
    """
    Extract email addresses from an Excel file containing WoS records.
    
    Args:
    - file_path (str): Path to the Excel file.
    - email_column (str or None): Column name containing emails (if known). If None, search entire file.
    
    Returns:
    - list: A list of extracted email addresses.
    """
    # Load the Excel file into a DataFrame
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error loading file: {e}")
        return []
    
    # If a specific column for emails is provided
    if email_column and email_column in df.columns:
        text_data = df[email_column].astype(str).tolist()
    else:
        # Concatenate all columns to search for emails
        text_data = df.astype(str).apply(lambda x: ' '.join(x), axis=1).tolist()
    
    # Regular expression for email pattern
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    # Find all emails in the data
    emails = set()
    for text in text_data:
        emails.update(re.findall(email_pattern, text))
    
    return list(emails)

# Example usage
if __name__ == "__main__":
    file_path = "Kitap1.xlsx"  # Replace with the actual file path
    email_column = None  # Set to a specific column name if you know it, e.g., "Author Emails"
    
    emails = extract_emails_from_excel(file_path, email_column)
    if emails:
        print("Extracted Email Addresses:")
        for email in emails:
            print(email)
    else:
        print("No email addresses found.")
