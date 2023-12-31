import chatgpt_rater
import pandas as pd
from tqdm import tqdm

def rate_many():
    rater = chatgpt_rater.GptSongRater()
    data = pd.read_csv('./subsample.csv')

    agency, narcissism, empathy, collectivism = [], [], [], []
    for lyrics in tqdm(data.lyrics):
        try:
            rate = rater.rate_song(lyrics)
            agency.append(rate['agency'])
            empathy.append(rate['empathy'])
            collectivism.append(rate['collectivism'])
            narcissism.append(rate['narcissism'])

        except Exception as e:
            print(e)
            agency.append(0)
            narcissism.append(0)
            empathy.append(0)
            collectivism.append(0)

    data['Agency'] = agency
    data['Narcissism'] = narcissism
    data['Collectivism'] = collectivism
    data['Empathy'] = empathy

    data.to_csv('./subsample_rated.csv')

if __name__ == '__main__':
    # rate_many()

    a = pd.read_csv('./subsample_rated.csv')
    g = a.groupby('year')
    m = g.mean(numeric_only=True).reset_index()

    import seaborn as sns
    from scipy import stats
    import matplotlib.pyplot as plt

    def r2(x, y):
        return stats.pearsonr(x, y)[0] ** 2

    for i in ['Empathy', 'Agency', 'Collectivism', 'Narcissism']:
        sns.jointplot(m, x='year', y=i, kind='reg')

        r, p = stats.pearsonr(x=m['year'], y = m[i])
        # annotate the pearson correlation coefficient text to 2 decimal places

        plt.savefig(f'{i}.png')
        plt.close('all')




