# Authors: Jakub Wirkus, Paweł Zborowski
# Description: Returns 6 movie recommendations for specified user based on user-based collaborative filtering
# Credits: https://realpython.com/build-recommendation-engine-collaborative-filtering/
# http://surpriselib.com/

from itertools import islice

import pandas as pd
from surprise import Reader, KNNBasic
from surprise import Dataset
from surprise import SVD


class MovieRecommender:
    """ Calculates recommended movies based on provided data set"""
    def __init__(self):
        self.movies = set()
        self.predictions = dict()
        self.ratings_dict = {'user': [], 'item': [], 'rating': []}
        self.csv = pd.read_csv("movieset.csv", encoding="Windows-1250", sep=';', header=None).fillna(0)

    def clean_data(self):
        """
        Prepares dataset for further processing.
        """
        for key, value in self.csv.iterrows():
            i = 0
            user = "usr"
            for col in value:
                if i == 0:
                    i += 1
                    user = col
                    continue
                else:
                    # movie
                    if i % 2 != 0:
                        if col != 0:
                            mov = col
                            self.ratings_dict['user'].append(user)
                            self.ratings_dict['item'].append(mov)
                    # rating
                    else:
                        if col != 0:
                            rat = col
                            self.ratings_dict['rating'].append(rat)
                    i += 1

    def __get_all_movies(self):
        """
        Extracts movies from provided dataset to set
        """
        for (columnName, columnData) in self.csv.iteritems():
            if columnName % 2 == 0:
                continue

            for movie in columnData:
                if movie == 0:
                    continue
                else:
                    self.movies.add(movie)

    def __get_user_rated_movies(self, user_id):
        movies_list = list()
        for key, value in self.csv.iterrows():
            if key != user_id:
                continue
            i = 0
            for col in value:
                if i == 0:
                    i += 1
                    continue
                else:
                    if i % 2 != 0:
                        if col != 0:
                            movies_list.append(col)
                    i += 1
        return movies_list

    def __get_username_id(self, username):
        for key, value in self.csv.iterrows():
            i = 0
            for col in value:
                if i == 0:
                    i += 1
                    if col == username:
                        return key
                else:
                    i += 1
                    continue

    @staticmethod
    def take(n, iterable):
        """
        Return first n items of the iterable as a list
        """
        return list(islice(iterable, n))

    def __recommend_movies(self, username):
        reader = Reader(rating_scale=(1, 10))
        df = pd.DataFrame(self.ratings_dict)
        data = Dataset.load_from_df(df[["user", "item", "rating"]], reader)
        sim_options = {
            "name": "cosine",
            'user_based': True,
            # 'min_support': 2
        }
        algo = KNNBasic(sim_options=sim_options)
        # algo = SVD()

        algo.fit(data.build_full_trainset())

        self.__get_all_movies()

        for movies in self.movies:
            prediction = algo.predict(username, movies)
            self.predictions[movies] = prediction.est

        for user_rated_movies in self.__get_user_rated_movies(self.__get_username_id(username)):
            del self.predictions[user_rated_movies]

    def get_recommended_movies(self, username):
        """
        Configures input values.
        :param username: Name and surname of user - Case sensitive
        :returns: dictionary of all recommended movies
        """
        self.__recommend_movies(username)
        return dict(sorted(self.predictions.items(), key=lambda item: item[1], reverse=True))

    def get_6_recommended_movies(self, username):
        """
        Configures input values.
        :param username: Name and surname of user - Case sensitive
        :returns: list of 6 recommended movies
        """
        self.__recommend_movies(username)
        return self.take(6, dict(sorted(self.predictions.items(), key=lambda item: item[1], reverse=True)))
