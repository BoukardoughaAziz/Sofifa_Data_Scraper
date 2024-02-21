import requests
from bs4 import BeautifulSoup
import csv

def scrape_player_data(url_base, player_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    url = f'{url_base}{player_url}'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        profile_div = soup.find('div', class_='profile clearfix')

        img_tag = profile_div.find('img', class_='loaded')
        image_link = img_tag.get('data-src') if img_tag else "N/A"

        player_id = player_url.split('/')[0]

        grid_divs = soup.find_all('div', class_='grid attribute')

        data = []  
        preferred_foot = "N/A"

        for grid_div in grid_divs:
            col_divs = grid_div.find_all('div', class_='col')
            for col_div in col_divs:
                p_tags = col_div.find_all('p')
                for p_tag in p_tags:
                    em_tag = p_tag.find('em', {'title': True})
                    if em_tag:
                        em_value = em_tag['title'].strip()
                        data.append(em_value)

                    if 'Left' in p_tag.text:
                        preferred_foot = 'Left'
                    elif 'Right' in p_tag.text:
                        preferred_foot = 'Right'

        with open('Performance.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)

            csv_writer.writerow(['Player_Id', 'image_link', 'Preferred_foot', 'Crossing', 'Finishing', 'Heading_accuracy', 'Short_passing', 'Volleys', 'Dribbling', 'Curve', 'FK_Accuracy', 'Long_passing', 'Ball_control', 'Acceleration', 'Sprint_speed', 'Agility', 'Reactions', 'Balance', 'Shot_power', 'Jumping', 'Stamina', 'Strength', 'Long shots', 'Aggression', 'Interceptions', 'Att. Position', 'Vision', 'Penalties', 'Composure', 'Defensive awareness', 'Standing tackle', 'Sliding tackle', 'GK Diving', 'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes'])

            if data:
                csv_writer.writerow([player_id, image_link, preferred_foot] + data)
    else:
        print(f"Failed to retrieve the page {url}. Status code: {response.status_code}")

url_base = 'https://sofifa.com/player/'
player_url = '252008/israel-reyes/240027/'

scrape_player_data(url_base, player_url)
