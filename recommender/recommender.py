import numpy as np
import pandas as pd


########
###
###  PART I Build the data
###
########



# 1. Get the Data
##### Set up column names for the csv file and create a data frame
##### This is currently just in a flat file and should be moved to a db asap
##### along with any other dataset I can find
def get_data():
    column_names = ['user_id', 'item_id', 'rating', 'timestamp']
    data_frame = pd.read_csv('.data/u.data', sep = '\t', names = column_names)
    return data_frame


# 2. Get Movie Titles
##### Get a list of the movie titles to go along with the previous data
##### Eventually this will just be a column on the movie's row in the db
##### and this function won't be needed
def get_movie_titles():
    movie_titles = pd.read_csv('.data/Movie_Id_Titles')
    return movie_titles

# 3. Merge Title
##### Merge the title column from the movie titles dataframe into the movie dataframe
##### Again, this won't be needed when the db holds everything, this is
##### just to compensate for flat files
def merge_titles(movies, titles):
    df = pd.merge(movies, titles)
    return df

# 4. Get Base Data
##### Returns the base movie dataframe as an easy function to call
def get_base_data():
    movies = get_data()
    titles = get_movie_titles()
    data = merge_titles(movies, titles)
    return data


# 5. Set Up Data
##### Sets up the data to be worked with, this whole process
##### will have to change as the project grows
def set_up_data():
    data = get_base_data()
    ratings = pd.DataFrame(data.groupby('title')['rating'].mean()) # Group the new frame by title and rating
    ratings['number of ratings'] = pd.DataFrame(data.groupby('title')['rating'].count()) # Add a new column for the num of ratings
    return ratings



########
###
###  PART II Build the system
###
########



# 1. Create Movie Matrix
##### Create a matrix with the title, user id of the movie and the rating of the movie
#####
def create_movie_matrix(base, ratings):
    matrix = base.pivot_table(index = 'user_id', columns = 'title', values = 'rating')
    return matrix

# 2. Sort Matrix
##### Sort matrix by number of ratings and rating on the ratings dataframe
#####
def sort_matrix(matrix):
    ratings = set_up_data()
    return ratings.sort_values('number of ratings', ascending = False)

# 3. Get User Ratings
##### Get user ratings on a given movie in a given matrix
##### takes matrix and title
def get_user_ratings(matrix, title):
    return matrix[title]

# 4. Get Ratings Correlation
##### Get the similar movies to the given movie
##### using the title we create the movie matrix and use pandas to correlation the data
##### After we get the correlation we need to filter out responses that don't make sense by
##### restricting the ratings count to a minimum of 100
def get_ratings_correlation(title):
    base_data = get_base_data()
    ratings = set_up_data()
    matrix = create_movie_matrix(base_data, ratings)
    user_ratings = get_user_ratings(matrix, title)
    similar = matrix.corrwith(user_ratings)
    correlation = pd.DataFrame(similar, columns = ['Correlation'])
    correlation.dropna(inplace = True) # @TODO: Look this up
    correlation = correlation.join(ratings['number of ratings']) # Add ratings count
    correlation = correlation[correlation['number of ratings'] > 100].sort_values('Correlation', ascending = False) # Filter by ratings count
    return correlation

