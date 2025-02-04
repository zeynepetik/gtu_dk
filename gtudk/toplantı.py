import requests
import pandas as pd
import time

def fetch_metadata_via_crossref(title):
    """
    Fetch metadata including authors' affiliations and emails using CrossRef API.
    """
    try:
        # Query CrossRef API
        response = requests.get(
            "https://api.crossref.org/works",
            params={"query.bibliographic": title, "rows": 1}
        )
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()

        # Check if metadata exists
        if data['message']['items']:
            # Get the first result
            article = data['message']['items'][0]
            authors = article.get('author', [])
            result = []

            # Process authors' information
            for author in authors:
                name = f"{author.get('given', '')} {author.get('family', '')}".strip()
                affiliation = "; ".join([aff.get('name', '') for aff in author.get('affiliation', [])])
                email = author.get('email', 'N/A')  # Emails are not always provided
                result.append({"Name": name, "Affiliation": affiliation, "Email": email})
            
            # Return the data as a DataFrame
            return pd.DataFrame(result)
        else:
            return pd.DataFrame(columns=["Name", "Affiliation", "Email"])
    except Exception as e:
        print(f"Error fetching data for title '{title}': {e}")
        return pd.DataFrame(columns=["Name", "Affiliation", "Email"])


def process_excel(file_path, output_file):
    """
    Read an Excel file, query CrossRef API for metadata, and save the results.
    """
    try:
        df = pd.read_excel(file_path)

        # Check for required column
        if 'Article Title' not in df.columns:
            raise ValueError("The input Excel file does not contain an 'Article Title' column.")

        # Create new columns
        df['Author Emails and Affiliations'] = None

        for index, row in df.iterrows():
            paper_title = row.get('Article Title', None)
            if paper_title:
                print(f"Processing row {index + 1}: {paper_title}")
                try:
                    author_data = fetch_metadata_via_crossref(paper_title)
                    
                    # Convert author data to a string for saving in the Excel file
                    if not author_data.empty:
                        df.at[index, 'Author Emails and Affiliations'] = author_data.to_string(index=False)
                    else:
                        df.at[index, 'Author Emails and Affiliations'] = "No metadata found"
                except Exception as e:
                    print(f"Error processing row {index + 1}: {e}")
                    df.at[index, 'Author Emails and Affiliations'] = f"Error: {e}"
                
                # Avoid hitting rate limits
                time.sleep(1)
        
        df.to_excel(output_file, index=False)
        print(f"Results saved to {output_file}")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    input_file = "Kitap1.xlsx"  # Input Excel file
    output_file = "output_metadata.xlsx"  # Output Excel file

    process_excel(input_file, output_file)
