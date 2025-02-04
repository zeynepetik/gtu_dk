import pandas as pd
from scholarly import scholarly

def search_authors_by_affiliation(affiliation):
    # Search for authors by affiliation using the scholarly library
    authors = []
    search_query = scholarly.search_author(f"{affiliation}")
    try:
        for author in search_query:
            # Collect author details
            author_info = scholarly.fill(author)
            author_data = {
                "Name": author_info.get("name", ""),
                "Affiliation": author_info.get("affiliation", ""),
                "Interests": ", ".join(author_info.get("interests", [])),
                "Email": author_info.get("email", "Not Available"),
                "Citations": author_info.get("citedby", 0),
                "Scholar ID": author_info.get("scholar_id", ""),
            }
            authors.append(author_data)
    except Exception as e:
        print(f"Error during data collection: {e}")
    return authors

def main():
    # Specify the university
    affiliation = "Gebze Technical University"
    print(f"Collecting data for authors affiliated with {affiliation}...")
    
    # Collect authors data
    authors = search_authors_by_affiliation(affiliation)
    
    # Sort authors by citation count in descending order
    sorted_authors = sorted(authors, key=lambda x: x["Citations"], reverse=True)
    
    # Get the top 10 authors
    top_authors = sorted_authors[:10]
    
    # Save data to an Excel file
    df = pd.DataFrame(top_authors)
    output_file = "GTU_top_10_scholars.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()
