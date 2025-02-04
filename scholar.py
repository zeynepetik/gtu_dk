import scholarly
import csv

def fetch_scholars(university_name, output_file="scholars_info.csv"):
    """
    Fetch scholar information from Google Scholar for a specific university.

    Args:
        university_name (str): Name of the university to search for scholars.
        output_file (str): Path to save the collected scholar information.
    """
    print(f"Searching for scholars affiliated with {university_name}...")
    
    # Search for the university and iterate through its scholars
    search_query = scholarly.search_facet(f"affiliation:{university_name}")
    scholars = []
    
    try:
        for scholar in search_query:
            print(f"Fetching data for: {scholar['name']}")
            author = scholarly.fill(scholar)  # Fetch detailed info for the scholar
            scholars.append({
                "Name": author.get("name", ""),
                "Affiliation": author.get("affiliation", ""),
                "Interests": ", ".join(author.get("interests", [])),
                "Citations": author.get("citedby", 0),
                "h-index": author.get("hindex", 0),
                "i10-index": author.get("i10index", 0),
                "Scholar ID": author.get("scholar_id", ""),
            })
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # Save the data to a CSV file
    with open(output_file, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=scholars[0].keys())
        writer.writeheader()
        writer.writerows(scholars)
    
    print(f"Data collected and saved to {output_file}")

if __name__ == "__main__":
    university_name = "Gebze Technical University"
    fetch_scholars(university_name)