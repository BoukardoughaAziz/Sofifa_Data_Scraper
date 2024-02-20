import requests
from bs4 import BeautifulSoup
import csv

def scrape_player_data(url_base, player_urls):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    all_player_data = []

    for player_url in player_urls:
        url = f'{url_base}{player_url}'

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the div with class 'profile clearfix'
            profile_div = soup.find('div', class_='profile clearfix')

            # Extract image link from img tag
            img_tag = profile_div.find('img', class_='loaded')
            image_link = img_tag.get('data-src') if img_tag else "N/A"

            # Find all divs with class 'grid attribute'
            grid_divs = soup.find_all('div', class_='grid attribute')

            data = []  # Initialize data list for each player
            # Extract values from em tags inside p tags
            for grid_div in grid_divs:
                col_divs = grid_div.find_all('div', class_='col')
                for col_div in col_divs:
                    p_tags = col_div.find_all('p')
                    for p_tag in p_tags:
                        em_tag = p_tag.find('em', {'title': True})
                        if em_tag:
                            em_value = em_tag['title'].strip()
                            data.append(em_value)

            # Append the complete data for each player to the overall data list
            all_player_data.append([image_link] + data)

        else:
            print(f"Failed to retrieve the page {url}. Status code: {response.status_code}")

    # Open CSV file for writing
    with open('output2.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header row (first column values become headers)
        csv_writer.writerow(['image_link', 'Crossing', 'Finishing', 'Heading accuracy', 'Short passing', 'Volleys', 'Dribbling', 'Curve', 'FK Accuracy', 'Long passing', 'Ball control', 'Acceleration', 'Sprint speed', 'Agility', 'Reactions', 'Balance', 'Shot power', 'Jumping', 'Stamina', 'Strength', 'Long shots', 'Aggression', 'Interceptions', 'Att. Position', 'Vision', 'Penalties', 'Composure', 'Defensive awareness', 'Standing tackle', 'Sliding tackle', 'GK Diving', 'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes'])

        # Write all collected data to CSV in a single row
        if all_player_data:
            csv_writer.writerows(all_player_data)

url_base = 'https://sofifa.com/player/'
player_urls = [
    '259240/adam-wharton/240027/',
    '255971/santiago-hezze/240001/'
]

scrape_player_data(url_base, player_urls)
