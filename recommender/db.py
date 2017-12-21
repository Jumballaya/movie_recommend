from pg import DB


db = DB(dbname = 'test', host = 'localhost', port = 5432, user = 'postgres', passwd = 'password')
if ('public.movies' not in db.get_tables()):
    db.query('create table movies(id serial primary key, title varchar UNIQUE, imdb_url varchar, rating decimal, ratings_count integer)')



def insert_movie(title, imdb_url, rating, ratings_count):
    db.insert('movies', title = title, imdb_url = imdb_url, rating = rating, ratings_count = ratings_count)
