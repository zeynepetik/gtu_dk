import scholarly

# Function to fetch and save article URLs
def fetch_article_urls(author_id, output_file):
    # Search for the author by their Google Scholar ID
    search_query = scholarly.search_author_id(author_id)
    author = scholarly.fill(search_query)

    # Open the output file in write mode
    with open(output_file, 'w') as file:
        # Iterate through the author's publications
        for publication in author['publications']:
            # Fill in the publication details
            pub = scholarly.fill(publication)
            # Extract the URL if available
            url = pub.get('eprint_url')
            if url:
                # Write the URL to the file
                file.write(url + '\n')
            else:
                print(f"No URL found for: {pub['bib']['title']}")

# Replace with the actual author ID from the Google Scholar profile URL
author_id = '1qKw6SIAAAAJ'
# Specify the output file name
output_file = 'article_urls.txt'

# Fetch and save the article URLs
fetch_article_urls(author_id, output_file)
