from recommender import set_up_data
import db


########
###
###  PART III Hook it up to a database
###
########




# 1. Create Movie List
##### Create a list of movie dict objects
#####
def create_movie_list():
    ratings = set_up_data()
    title_list = list()
    rating_list = list()
    num_rating_list = list()

    for title in ratings.index:
        title_list.append(title)

    for rating in ratings['rating']:
        rating_list.append(rating)

    for num in ratings['number of ratings']:
        num_rating_list.append(num)

    movie_list = list()

    for i in range(len(ratings)):
        movie = {}
        movie['title'] = title_list[i]
        movie['rating'] = rating_list[i]
        movie['ratings_count'] = num_rating_list[i]
        movie['imdb_url'] = 'https://www.imdb.com'
        movie_list.append(movie)

    return movie_list


# 2. Upload Movies
##### Upload movies to database
#####
def upload_movies():
    movie_list = create_movie_list()
    for movie in movie_list:
        title = movie['title']
        imdb_url = movie['imdb_url']
        rating = movie['rating']
        ratings_count = movie['ratings_count']
        db.insert_movie(title, imdb_url, rating, ratings_count)


upload_movies()
