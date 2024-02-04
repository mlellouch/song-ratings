import requests
import csv
from bs4 import BeautifulSoup
from pathlib import Path
from tqdm import tqdm
import time
import pandas as pd

class DiscogsRetreiver:
    pass


class UMDRetriever:

    def __init__(self):
        self.page = 'http://www.umdmusic.com/'

    def parse_url(self, url: str):
        html = requests.get(self.page + url).text
        bs = BeautifulSoup(html, features='html.parser')
        table = bs.findAll('table')[9]
        new_songs = []
        for new_song in table.findAll(name='tr', attrs={'bgcolor': '#66CCFF'}):
            try:
                columns = new_song.findAll(name='td')
                song_name, artist = list(columns[4].stripped_strings)
                year = columns[5].text.strip().split('-')[0]
                new_songs.append((song_name, artist, year))
            except:
                pass

        next_page = bs.findAll("b", string='Next Chart')
        if len(next_page) == 0:
            return new_songs, None
        else:
            next_page = next_page[0].parent['href']
            return new_songs, next_page


    def get_songs(self, start_url: str):
        current_url = start_url
        while True:
            try:
                if current_url is None:
                    break
                new_songs, current_url = self.parse_url(current_url)
                for song in new_songs:
                    yield song

                time.sleep(0.1)
            except:
                continue

    def filter_duplicates(self, file_path: Path):
        data = pd.read_csv(file_path, encoding='unicode_escape')
        data.drop_duplicates(inplace=True)
        filtered_path = file_path.parent / Path(file_path.parts[-1].replace('.csv', '_filtered.csv'))
        data.to_csv(filtered_path, index=False)


    def run(self, start_url: str, file_name: 'us_singles.csv'):
        file_path = Path(__file__).parent / Path('song_names') / Path(file_name)
        with open(file_path, 'a', newline='') as fp:
            writer = csv.DictWriter(f=fp, fieldnames=['name', 'artist', 'year'])
            writer.writeheader()
            for (name, arist, year) in tqdm(self.get_songs(start_url=start_url), desc='running umd retriever'):
                try:
                    writer.writerow({'name': name, 'artist': arist, 'year': year})
                except UnicodeEncodeError:
                    continue
                fp.flush()

        self.filter_duplicates(file_path=file_path)



if __name__ == '__main__':
    us_singles = 'default.asp?Lang=English&Chart=D&ChDay=&ChMonth=&ChYear=1940&ChBand=&ChSong='
    uk_singles = 'default.asp?Lang=English&Chart=A&ChDay=&ChMonth=&ChYear=192&ChBand=&ChSong='
    # us_albums = 'default.asp?Lang=English&Chart=E&ChDate=19701226&ChMode=P'
    us_albums = 'default.asp?Lang=English&Chart=E&ChDate=20141227&ChMode=N'

    test = 'default.asp?Lang=English&Chart=D'
    UMDRetriever().run(test, file_name='test.csv')
