import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
from pathlib import Path
from tqdm import tqdm
from multiprocessing import Process, Queue
import multiprocessing
import queue


def get_lyrics_process(in_message_queue: Queue, out_message_queue: Queue):
    driver = selenium.webdriver.Firefox()

    def get_lyrics(song_name, artist):
        driver.get('https://lyrics.lyricfind.com/')
        search_bar = driver.find_element(by=By.ID, value="search-field")
        search_bar.send_keys(f'{song_name} {artist}')
        time.sleep(4)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(6)
        try:
            lyrics_element = driver.find_element(by=By.CLASS_NAME, value='css-165casq')
        except selenium.common.exceptions.NoSuchElementException:
            return None
        return lyrics_element.text

    try:
        name, artist, year = in_message_queue.get(block=True)
        while True:
            lyrics = get_lyrics(song_name=name, artist=artist)
            out_message_queue.put([name, artist, year, lyrics])
            name, artist, year = in_message_queue.get(timeout=5.0)
    except queue.Empty:
        print('end')
        return

class LyricRetriever:

    def __init__(self):
        self.driver = selenium.webdriver.Firefox()

    def get_lyrics(self, song_name, artist):
        self.driver.get('https://lyrics.lyricfind.com/')
        search_bar = self.driver.find_element(by=By.ID, value="search-field")
        search_bar.send_keys(f'{song_name} {artist}')
        time.sleep(4)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(6)
        try:
            lyrics_element = self.driver.find_element(by=By.CLASS_NAME, value='css-165casq')
        except selenium.common.exceptions.NoSuchElementException:
            return None
        return lyrics_element.text

    def run_process(self, in_message_queue: Queue, out_message_queue: Queue):
        print('start')
        try:
            while True:
                name, artist, year = in_message_queue.get(timeout=5.0)
                print(f'got {name}')
                lyrics = self.get_lyrics(song_name=name, artist=artist)
                out_message_queue.put([name, artist, year, lyrics])
        except queue.Empty:
            print('end')
            return


class LyricsProcessor:

    def run(self):
        retriever = LyricRetriever()
        with open(Path(__file__).parent / Path('./song_names/us_singles_filtered.csv'), 'r') as read:
            with open(Path(__file__).parent / Path('./song_lyrics/us_singles_filtered'), 'w', newline='') as write:
                reader = csv.DictReader(f=read)
                writer = csv.DictWriter(f=write, fieldnames=['name','artist','year', 'lyrics'])
                writer.writeheader()
                for row in tqdm(reader, desc='getting lyrics'):
                    lyrics = retriever.get_lyrics(song_name=row['name'], artist=row['artist'])
                    if lyrics is not None:
                        writer.writerow({
                            'name': row['name'],
                            'artist': row['artist'],
                            'year': row['year'],
                            'lyrics': f'"{lyrics}"'
                        })
                    else:
                        writer.writerow({
                            'name': row['name'],
                            'artist': row['artist'],
                            'year': row['year'],
                            'lyrics': '""'
                        })
                    write.flush()

    def run_parallel(self, number_of_processes: int):
        in_message_queue = Queue()
        out_message_queue = Queue()

        with open(Path(__file__).parent / Path('./song_names/us_singles_filtered.csv'), 'r', encoding="utf8") as read:
            with open(Path(__file__).parent / Path('./song_lyrics/us_singles_filtered.csv'), 'w', newline='', encoding="utf8") as write:
                reader = csv.DictReader(f=read)
                for row in tqdm(reader, desc='putting lyrics in queue'):
                    in_message_queue.put([row['name'], row['artist'], row['year']])

                counter = tqdm(desc='retreiving lyrics')
                writer = csv.DictWriter(f=write, fieldnames=['name','artist','year', 'lyrics'])
                writer.writeheader()

                procs = [Process(target=get_lyrics_process, args=(in_message_queue, out_message_queue)) for _ in range(number_of_processes)]
                [proc.start() for proc in procs]
                while any([p.is_alive() for p in procs]):
                    while not out_message_queue.empty():
                        name, artist, year, lyrics = out_message_queue.get()
                        writer.writerow({
                            'name': name,
                            'artist': artist,
                            'year': year,
                            'lyrics': lyrics
                        })

                        counter.update(1)
                    write.flush()


if __name__ == '__main__':
    LyricsProcessor().run_parallel(number_of_processes=8)
