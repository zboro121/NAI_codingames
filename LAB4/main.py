# Authors: Jakub Wirkus, Paweł Zborowski
# Description: Returns 6 movie recommendations for specified user based on user-based collaborative filtering
# Credits: https://realpython.com/build-recommendation-engine-collaborative-filtering/
# http://surpriselib.com/

from LAB4.moviesRecomender import MovieRecommender

mr = MovieRecommender()
mr.clean_data()

print('6 recommended movies:', mr.get_6_recommended_movies('user1'))
# print(mr.get_recommended_movies('user1'))

