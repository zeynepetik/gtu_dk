import pandas as pd

# Load the Excel file
file_path = 'savedrecs.xlsx'  # Replace with the actual file path
df = pd.read_excel(file_path)

# Display the first few rows to understand the structure
print("DataFrame Head:")
print(df.head())

# Check for the presence of required columns
required_columns = ['Author Full Names', 'Affiliations', 'Email Addresses']  # Replace with your actual column names
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    print(f"Error: The following required columns are missing from the Excel file: {missing_columns}")
else:
    # Filter rows where Email Addresses is empty or NaN
    no_email_info = df[df['Email Addresses'].isna() | (df['Email Addresses'].str.strip() == '')]

    if no_email_info.empty:
        print("\nNo rows found without email addresses.")
    else:
        # Create a new DataFrame with the required columns for people without email addresses
        extracted_info = no_email_info[required_columns]

        # Display the extracted information
        print("\nExtracted Information (People Without Email Addresses):")
        print(extracted_info)

        # Save the extracted information to a new Excel file
        output_file_path = 'no_email_extracted.xlsx'
        extracted_info.to_excel(output_file_path, index=False)
        print(f"\nExtracted information has been saved to {output_file_path}")
