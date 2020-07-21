import pandas as pd


class Dictionary(object):

    @property
    def get_dict(self):
        header = ['code', 'title', 'year', 'genres']
        file_path = '.\\movies.csv'
        df = pd.read_csv(file_path, names=header)
        df = df.drop([0])
        code = df['code']
        titles = df['title']
        movies = {}
        for i in df.index:
            movies[code[i]] = titles[i]
        return movies
