import chatgpt_rater_rosenberg
import pandas as pd
from tqdm import tqdm

def rate_many():
    rater = chatgpt_rater_rosenberg.GptSongRater()
    data = pd.read_csv('./subsubsample.csv')

    self_esteem = []
    for lyrics in tqdm(data.lyrics):
        try:
            rate = rater.rate_song(lyrics)
            self_esteem.append(rate['self-esteem'])
        except Exception as e:
            print(e)
            self_esteem.append(0)

    data['Self_Esteem'] = self_esteem
    data.to_csv('./subsample_rated.csv')

def rate_many_rosenberg():
    rater = chatgpt_rater_rosenberg.RosenbergSongRater()
    data = pd.read_csv('./subsubsample.csv')

    answers = []
    for lyrics in tqdm(data.lyrics):
        try:
            rate = rater.rate_song(lyrics)
            vals = {
                'strongly agree': 4,
                'agree': 3,
                'disagree': 2,
                'strongly disagree': 1,
            }

            s = {}
            for k, v in rate.items():
                s[k] = vals[v]

            answers.append(s)

        except Exception as e:
            print(e)
            answers.append({'on the whole, i am satisfied with myself.': 0,
                             'at times i think i am no good at all.': 0,
                             'i feel that i have a number of good qualities.': 0,
                             'i am able to do things as well as most other people.': 0,
                             'i feel i do not have much to be proud of.': 0,
                             'i certainly feel useless at times.': 0,
                             "i feel that i'm a person of worth, at least on an equal plane with others.":  0,
                             'i wish i could have more respect for myself.': 0,
                             'all in all, i am inclined to feel that i am a failure.': 0,
                            'i take a positive attitude toward myself.': 0})

    new_data = pd.DataFrame(answers)
    new_data.to_csv('./rosenberg.csv')

if __name__ == '__main__':
    rate_many_rosenberg()

    # a = pd.read_csv('./subsample_rated.csv')
    # g = a.groupby('year')
    # m = g.mean(numeric_only=True).reset_index()
    #
    # import seaborn as sns
    # from scipy import stats
    # import matplotlib.pyplot as plt
    #
    # def r2(x, y):
    #     return stats.pearsonr(x, y)[0] ** 2
    #
    # for i in ['Empathy', 'Agency', 'Collectivism', 'Narcissism']:
    #     sns.jointplot(m, x='year', y=i, kind='reg')
    #
    #     r, p = stats.pearsonr(x=m['year'], y = m[i])
    #     # annotate the pearson correlation coefficient text to 2 decimal places
    #
    #     plt.savefig(f'{i}.png')
    #     plt.close('all')




