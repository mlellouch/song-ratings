import openai
import json
import os

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
                    "content": ":You are an intelligent psychologist, that is asked to label song lyrics, on the following criteria\n"
                               "self-esteem - Self-esteem is confidence in one's own worth, abilities, or morals."
                               "For each song lyrics that you will be given, return only a json object, that will contain the ratings of each criteria from 1 to 4"
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

class RosenbergSongRater:
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
                    "content": ":You are an intelligent psychologist. You will be given song lyrics, and you need to imagine what the author of the lyrics would have answered to statements."
                               "The only possible answers are Strongly Agree, Agree, Disagree, Strongly Disagree.\n"
                               "The statements are:\n"
                               "On the whole, I am satisfied with myself.\n"
                               "At times I think I am no good at all.\n"
                               "I feel that I have a number of good qualities.\n"
                               "I am able to do things as well as most other people.\n"
                               "I feel I do not have much to be proud of.\n"
                               "I certainly feel useless at times.\n"
                               "I feel that I'm a person of worth, at least on an equal plane with others.\n"
                               "I wish I could have more respect for myself.\n"
                               "All in all, I am inclined to feel that I am a failure.\n"
                               "I take a positive attitude toward myself.\n"
                               "For each song lyrics that you will be given, return only a json object, that will contain the answer of each statement. The fields should be the statements, exactly as stated."
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

    song = "I love myself so much, so very very much\n" \
           "And I love communism, it is literally the best thing in the world\n" \
           "However, it seems I can't change nothing in this world,\n" \
           "Like me, all those poor souls of this world, I can feel their pain"

    rate = rater.rate_song(song_lyrics=song)
    print(rate)

