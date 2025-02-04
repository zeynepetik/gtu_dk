from scholarly import scholarly

def fetch_researcher_profiles(query):
    try:
        print(f"Searching for researchers related to: '{query}'\n")
        # Search for authors matching the query
        search_query = scholarly.search_author(query)
        
        for author in search_query:
            print("Author Name:", author['name'])
            print("Affiliation:", author.get('affiliation', 'N/A'))
            print("Research Interests:", ", ".join(author.get('interests', [])))
            print("Citations:", author.get('citedby', 'N/A'))
            print("Profile Link:", f"https://scholar.google.com{author['url_picture']}" if 'url_picture' in author else "N/A")
            print("-" * 50)
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    query = input("Enter a research topic or researcher name to search: ")
    fetch_researcher_profiles(query)
