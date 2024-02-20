import requests
from bs4 import BeautifulSoup
import csv

def scrape_data(url_base, max_offset):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    all_player_data = []

    for offset in range(0, max_offset + 1, 60):

        url = f'{url_base}?offset={offset}'

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            table = soup.find('table')

            if table:
                for row in table.find_all('tr')[1:]:
                    columns = row.find_all('td')

                    age_info = columns[1].text.strip()
                    FirstName, name_with_positions = age_info.split(None, 1)

                    name_parts = name_with_positions.split()
                    playing_positions = ' '.join(name_parts[1:])

                    # Extract contract years, handling potential line breaks
                    team_and_contract = columns[5].text.strip()
                    contract_years = team_and_contract.splitlines()[-1].strip()  # Get the last line

                    # Extract profile link
                    profile_link = columns[1].find('a')['href']
                    full_profile_link = f'https://sofifa.com{profile_link}'  # Concatenate the base URL

                    player_data = {
                        'LastName': name_parts[0],
                        'FirstName': FirstName,
                        'age': columns[2].text.strip(),
                        'Overall Rating': columns[3].text.strip(),
                        'Potential Rating': columns[4].text.strip(),
                        'Team': team_and_contract.splitlines()[0].strip(),
                        'Contract Value': columns[6].text.strip(),
                        'Wage': columns[7].text.strip(),
                        'Total Stats': columns[8].text.strip(),
                        'Playing Positions': playing_positions,
                        'Contract': contract_years,
                        'Profile Link': full_profile_link  # Use the full profile link
                    }

                    all_player_data.append(player_data)
            else:
                print(f"Error: Table not found on the page with offset {offset}. Skipping.")
        else:
            print(f"Error: Unable to retrieve data from the page with offset {offset}. Status code: {response.status_code}. Skipping.")

    with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['LastName', 'FirstName', 'age', 'Overall Rating', 'Potential Rating', 'Team', 'Contract Value', 'Wage', 'Total Stats', 'Playing Positions', 'Contract', 'Profile Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(all_player_data)

    print("Data successfully written to output.csv")

url_base = 'https://sofifa.com/players'
max_offset = 1200
scrape_data(url_base, max_offset)
