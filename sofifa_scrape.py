import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_data(url_base, max_offset):
    start_time = time.time()  

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

                    team_and_contract = columns[5].text.strip()
                    contract_years = team_and_contract.splitlines()[-1].strip()  

                    profile_link = columns[1].find('a')['href'].replace('/player/', '')  
                    player_id = profile_link.split('/')[0]

                    player_data = {
                        'Player_Id': player_id,
                        'LastName': name_parts[0],
                        'FirstName': FirstName,
                        'age': columns[2].text.strip(),
                        'Overall_Rating': columns[3].text.strip(),
                        'Potential_Rating': columns[4].text.strip(),
                        'Team': team_and_contract.splitlines()[0].strip(),
                        'Contract_Value': columns[6].text.strip(),
                        'Wage': columns[7].text.strip(),
                        'Total_Stats': columns[8].text.strip(),
                        'Playing_Positions': playing_positions,
                        'Contract': contract_years,
                        'Profile_Link': profile_link  
                    }

                    all_player_data.append(player_data)
            else:
                print(f"Error: Table not found on the page with offset {offset}. Skipping.")
        else:
            print(f"Error: Unable to retrieve data from the page with offset {offset}. Status code: {response.status_code}. Skipping.")

    with open('Players.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Player_Id', 'LastName', 'FirstName', 'age', 'Overall_Rating', 'Potential_Rating', 'Team', 'Contract_Value', 'Wage', 'Total_Stats', 'Playing_Positions', 'Contract', 'Profile_Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(all_player_data)

    end_time = time.time()  
    elapsed_time = end_time - start_time
    print(f"Data successfully written to Players.csv\nTime taken: {elapsed_time:.2f} seconds")

url_base = 'https://sofifa.com/players'
max_offset = 1200
scrape_data(url_base, max_offset)
