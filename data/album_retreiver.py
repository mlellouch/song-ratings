import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
from pathlib import Path
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup

class AlbumRetrierver:

    def __init__(self):
        options = selenium.webdriver.FirefoxOptions()
        options.add_argument('disable-infobars')
        self.driver = selenium.webdriver.Firefox()
        self.driver.set_page_load_timeout(5)


    def find_album(self, album_name, artist):
        try:
            self.driver.get(url=f'https://www.discogs.com/search/?q={album_name.replace(" ", "+")}+{artist}&type=master')
        except selenium.common.exceptions.TimeoutException:
            pass
        bs = BeautifulSoup(self.driver.page_source, features='html.parser')
        first_result_url = bs.findAll('ul', attrs={'class': 'cards'})[0].findAll('a')[0]['href']

        try:
            self.driver.get(url='https://www.discogs.com' + first_result_url)
        except selenium.common.exceptions.TimeoutException:
            pass

        bs = BeautifulSoup(self.driver.page_source, features='html.parser')
        genre_table = bs.findAll('table', attrs={'class': 'table_1fWaB'})[0]
        genre = genre_table.findAll('td')[0].text
        style = genre_table.findAll('td')[1].text

        tracklist = bs.findAll('section', attrs={'id': "release-tracklist"})[0]
        all_tracks = tracklist.findAll('td', attrs={'class': 'trackTitleNoArtist_ANE8Q'})
        all_track_names = [track.text for track in all_tracks]
        return all_track_names, genre, style


    def run(self, source: Path, dest: Path):
        with open(source, 'r') as read_file:
            reader = csv.DictReader(read_file)
            with open(dest, 'w', newline='') as write_file:
                writer = csv.DictWriter(write_file, fieldnames=['name', 'artist', 'year', 'genre', 'style'])
                writer.writeheader()
                for line in tqdm(reader):
                    try:
                        songs, genre, style = self.find_album(line['name'], line['artist'])
                    except:
                        print(f'failed {line["name"]}, {line["artist"]}')
                        continue
                    for song in songs:
                        writer.writerow({
                            'name': song,
                            'artist': line['artist'],
                            'year': line['year'],
                            'genre': genre,
                            'style': style
                        })

                        write_file.flush()



if __name__ == '__main__':
    AlbumRetrierver().run(source=Path('./song_names/us_albums_filtered.csv'), dest=Path('./song_names/us_album_songs.csv'))



