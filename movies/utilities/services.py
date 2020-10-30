from typing import Iterable
import random

import json
import urllib.parse

from movies.adapters.repository import AbstractRepository
from movies.domain.model import Movie


def get_genre_names(repo: AbstractRepository):
    genres = repo.get_genres()
    genre_names = [genre.genre_name for genre in genres]

    return genre_names


def get_random_movies(quantity, repo: AbstractRepository):
    movie_count = repo.get_number_of_movies()

    if quantity >= movie_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of movies.
        quantity = movie_count - 1

    # Pick distinct and random movies.
    random_ids = [1,2,3]
    movies = repo.get_movies_by_id(random_ids)

    return movies_to_dict(movies)



# ============================================
# Functions to convert dicts to model entities
# ============================================

def movie_to_dict(movie: Movie):
    # response = requests.get("https://v2.sg.media-imdb.com/suggests/"+movie.title.lower()[0]+"/"+urllib.parse.quote_plus(movie.title.lower())+".json").text
    hyp = movie.image_hyperlink
    # x = json.loads(response.split("(", 1)[1].strip(")"))
    # print("https://v2.sg.media-imdb.com/suggests/"+movie.title.lower()[0]+"/"+movie.title.lower()+".json")
    # for i in x["d"]:
    #     if "l" in i:
    #         if movie.title.lower() == i["l"].lower():
    #             if "y" in i and "i" in i:
    #                 if i["i"][0]:
    #                     hyp = i["i"][0]
    # print(hyp)
    movie_dict = {
        'id': movie.id,
        'date': movie.date,
        'title': movie.title,

        'first_para': movie.first_para,
        'hyperlink': movie.hyperlink,
        'rank': movie.rank,
        'director': movie.director,
        'time': movie.time,
        'rating': movie.rating,
        'actors': movie.actors,
        'image_hyperlink': hyp
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
