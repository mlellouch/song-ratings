import openai
import json

api_key = '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'

class GptSongRater:
    """
    This uses the assistant api. This assumes that the assitant has already been created (in the openAI online GUI)
    """

    def _find_assistant(self):
        assistants = self.client.beta.assistants.list()
        for assis in assistants:
            if assis.name == 'SongRater':
                return assis

        raise ValueError("assistant not found")

    def __init__(self):
        self.client = openai.OpenAI(api_key=api_key)

    def rate_song(self, song_lyrics):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an intelligent psychologist, that is asked to label song lyrics, on the following criteria:\n"
                               "Agency - the capacity of an actor to act in a given environment,\n"
                               "Empathy - the ability to understand and share the feelings of another.\n"
                               "Collectivism - the practice or principle of giving a group priority over each individual in it.\n"
                               "Narcissism - self–centered personality style characterized as having an excessive preoccupation with oneself and one's own needs, often at the expense of others.\n\n"
                               "For each song lyrics that you will be given, return only a json object, that will contain the ratings of each criteria from 1 to 7"
                },
                {
                    "role": "user",
                    "content": song_lyrics
                },
            ],
            temperature=0.31,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        json_text = response.choices[0].message.content
        return json.loads(json_text.lower())


if __name__ == '__main__':
    rater = GptSongRater()

    song = "I'm, too sexy for my shirt, too sexy for my shirt\n" \
           "Oh yeah\n" \
           "I'm, too sexy for your party, too sexy for your party\n" \
           "No way I'm disco dancing in your party.\n"

    rate = rater.rate_song(song_lyrics=song)
    print(rate)

