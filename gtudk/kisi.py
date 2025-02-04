import time
import pandas as pd
from scholarly import scholarly

def fetch_gtu_scholars():
    university_name = "Gebze Technical University"
    print(f"Searching for scholars affiliated with {university_name}...\n")

    # Initialize an empty DataFrame
    scholars_df = pd.DataFrame(columns=["Name", "Affiliation", "Interests", "Citations", "H-index", "i10-index", "Profile URL"])

    try:
        # Search for authors with the university name as a keyword
        search_query = scholarly.search_author(university_name)

        for author in search_query:
            # Get detailed information about the author
            author_info = scholarly.fill(author)
            # Check if the author's affiliation matches GTU
            if university_name.lower() in author_info.get("affiliation", "").lower():
                scholar_data = {
                    "Name": author_info.get("name"),
                    "Affiliation": author_info.get("affiliation"),
                    "Interests": ", ".join(author_info.get("interests", [])),
                    "Citations": author_info.get("citedby"),
                    "H-index": author_info.get("hindex"),
                    "i10-index": author_info.get("i10index"),
                    "Profile URL": author_info.get("url_picture"),
                }

                # Append the data directly to the DataFrame
                scholars_df = pd.concat([scholars_df, pd.DataFrame([scholar_data])], ignore_index=True)
                print(f"Fetched: {scholar_data['Name']}")

                # Introduce a delay to avoid excessive requests
                time.sleep(2)

    except Exception as e:
        print(f"Error occurred: {e}")

    return scholars_df

# Run the script
if __name__ == "__main__":
    scholars_df = fetch_gtu_scholars()

    if not scholars_df.empty:
        scholars_df.to_csv("GTU_Scholars.csv", index=False)
        print("\nScholar information saved to 'GTU_Scholars.csv'.")
    else:
        print("\nNo scholars found.")
