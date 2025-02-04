import requests
import pandas as pd
import time
from bs4 import BeautifulSoup


def fetch_metadata_and_emails(title):
    """
    Fetch metadata using CrossRef and attempt to scrape email addresses from article's landing page.
    """
    try:
        # Query CrossRef API
        response = requests.get(
            "https://api.crossref.org/works",
            params={"query.bibliographic": title, "rows": 1}
        )
        response.raise_for_status()
        data = response.json()

        # Check if metadata exists
        if data['message']['items']:
            # Get the first result
            article = data['message']['items'][0]
            authors = article.get('author', [])
            url = article.get('URL', None)
            result = []

            # Fetch emails from the article's landing page if URL is available
            emails = get_emails_from_webpage(url) if url else set()

            # Process authors' information
            for author in authors:
                name = f"{author.get('given', '')} {author.get('family', '')}".strip()
                affiliation = "; ".join([aff.get('name', '') for aff in author.get('affiliation', [])])
                email = emails.pop() if emails else "N/A"
                result.append({"Name": name, "Affiliation": affiliation, "Email": email})
            
            # Return the data as a DataFrame
            return pd.DataFrame(result)
        else:
            return pd.DataFrame(columns=["Name", "Affiliation", "Email"])
    except Exception as e:
        print(f"Error fetching data for title '{title}': {e}")
        return pd.DataFrame(columns=["Name", "Affiliation", "Email"])


def get_emails_from_webpage(url):
    """
    Scrapes email addresses from an article's webpage.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        emails = set()
        for word in soup.get_text().split():
            if "@" in word and "." in word:  # Basic email pattern
                emails.add(word.strip())
        return emails
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return set()


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
                    author_data = fetch_metadata_and_emails(paper_title)
                    
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
    output_file = "output_emails.xlsx"  # Output Excel file

    process_excel(input_file, output_file)
