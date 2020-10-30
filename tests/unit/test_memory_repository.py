from datetime import date, datetime
from typing import List

import pytest

from movies.domain.model import User, Movie, Genre, Review, make_review
from movies.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()

    # Check that the query returned 6 Movies.
    assert number_of_movies == 1000


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie(
        date.fromisoformat('2016-01-01'),
        "2016-01-01 La La Land",
        "woooow grape",
        "http.google.com",
        "sasdf",
        1,
        "me",
        123,
        "also me",
        10,
    )
    in_memory_repo.add_movie(movie)

    assert movie is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)

    # Check that the Movie has the expected title.
    assert movie.title == 'Guardians of the Galaxy'

    # Check that the Movie is reviewed as expected.

def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(99999)
    assert movie is None


def test_repository_can_retrieve_movies_by_date(in_memory_repo):
    movies = in_memory_repo.get_movies_by_date(date(2020, 3, 1))

    # Check that the query returned 3 Movies.
    assert len(movies) == 0


def test_repository_does_not_retrieve_an_movie_when_there_are_no_movies_for_a_given_date(in_memory_repo):
    movies = in_memory_repo.get_movies_by_date(date(2020, 3, 8))
    assert len(movies) == 0


def test_repository_can_retrieve_genres(in_memory_repo):
    genres: List[Genre] = in_memory_repo.get_genres()

    assert len(genres) == 20

    genre_one = [genre for genre in genres if genre.genre_name == 'Action'][0]
    genre_two = [genre for genre in genres if genre.genre_name == 'Adventure'][0]
    genre_three = [genre for genre in genres if genre.genre_name == 'Horror'][0]
    genre_four = [genre for genre in genres if genre.genre_name == 'Thriller'][0]

    assert genre_one.number_of_genreged_movies == 303
    assert genre_two.number_of_genreged_movies == 259
    assert genre_three.number_of_genreged_movies == 119
    assert genre_four.number_of_genreged_movies == 195


def test_repository_can_get_first_movie(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    assert movie.title == 'Inland Empire'


def test_repository_can_get_last_movie(in_memory_repo):
    movie = in_memory_repo.get_last_movie()
    assert movie.title == 'The Black Room'


def test_repository_can_get_movies_by_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([2, 5, 6])

    assert len(movies) == 3
    assert movies[
               0].title == 'Prometheus'
    assert movies[1].title == "Suicide Squad"
    assert movies[2].title == 'The Great Wall'


def test_repository_does_not_retrieve_movie_for_non_existent_id(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([2, 9])

    assert len(movies) == 2
    assert movies[
               0].title == 'Prometheus'


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([0, 9])

    assert len(movies) == 1


def test_repository_returns_movie_ids_for_existing_genre(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_genre('Action')

    assert movie_ids == [1,
 5,
 6,
 9,
 13,
 15,
 18,
 25,
 27,
 30,
 33,
 34,
 35,
 36,
 38,
 39,
 46,
 49,
 51,
 52,
 54,
 55,
 61,
 66,
 68,
 70,
 72,
 76,
 77,
 79,
 80,
 81,
 85,
 86,
 88,
 90,
 92,
 95,
 96,
 102,
 105,
 108,
 111,
 114,
 118,
 124,
 125,
 127,
 135,
 141,
 148,
 150,
 154,
 156,
 157,
 159,
 160,
 162,
 163,
 164,
 165,
 167,
 169,
 170,
 176,
 177,
 178,
 180,
 195,
 196,
 200,
 201,
 204,
 205,
 206,
 211,
 213,
 214,
 215,
 216,
 217,
 218,
 220,
 221,
 228,
 229,
 233,
 234,
 235,
 240,
 241,
 244,
 249,
 254,
 257,
 258,
 265,
 269,
 271,
 273,
 276,
 277,
 280,
 282,
 285,
 286,
 287,
 288,
 289,
 291,
 295,
 301,
 302,
 309,
 316,
 317,
 318,
 320,
 323,
 324,
 326,
 332,
 335,
 341,
 342,
 343,
 345,
 346,
 356,
 363,
 369,
 370,
 371,
 372,
 373,
 374,
 376,
 380,
 385,
 386,
 387,
 388,
 389,
 390,
 391,
 392,
 397,
 401,
 403,
 409,
 411,
 415,
 421,
 423,
 424,
 425,
 427,
 428,
 430,
 433,
 434,
 435,
 439,
 447,
 449,
 451,
 453,
 454,
 455,
 466,
 467,
 469,
 470,
 473,
 483,
 485,
 492,
 493,
 494,
 497,
 501,
 512,
 517,
 518,
 523,
 526,
 527,
 529,
 530,
 533,
 534,
 536,
 537,
 538,
 543,
 553,
 558,
 559,
 561,
 565,
 567,
 576,
 577,
 578,
 579,
 581,
 582,
 586,
 588,
 597,
 598,
 600,
 601,
 602,
 604,
 610,
 616,
 618,
 619,
 622,
 625,
 626,
 627,
 650,
 658,
 661,
 664,
 674,
 675,
 677,
 680,
 681,
 684,
 688,
 691,
 694,
 699,
 703,
 705,
 711,
 719,
 725,
 729,
 738,
 740,
 742,
 754,
 759,
 760,
 764,
 767,
 768,
 771,
 772,
 773,
 778,
 781,
 782,
 788,
 790,
 795,
 800,
 803,
 804,
 807,
 810,
 811,
 823,
 828,
 829,
 834,
 838,
 845,
 855,
 857,
 870,
 872,
 873,
 879,
 880,
 881,
 893,
 895,
 896,
 902,
 904,
 905,
 917,
 921,
 922,
 924,
 925,
 936,
 939,
 945,
 949,
 955,
 957,
 959,
 969,
 970,
 991,
 994]


def test_repository_returns_an_empty_list_for_non_existent_genre(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_genre('Hello')

    assert len(movie_ids) == 0


def test_repository_returns_date_of_previous_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(6)
    previous_date = in_memory_repo.get_date_of_previous_movie(movie)

    assert previous_date.isoformat() == '2015-01-01'


def test_repository_returns_none_when_there_are_no_previous_movies(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    previous_date = in_memory_repo.get_date_of_previous_movie(movie)

    assert previous_date == date(2013, 1, 1)


def test_repository_returns_date_of_next_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(3)
    next_date = in_memory_repo.get_date_of_next_movie(movie)

    assert next_date.isoformat() == '2017-01-01'




def test_repository_can_add_a_genre(in_memory_repo):
    genre = Genre('Motoring')
    in_memory_repo.add_genre(genre)

    assert genre in in_memory_repo.get_genres()


def test_repository_can_add_a_review(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(2)
    review = make_review("Trump's onto it!", user, movie)

    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()


def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    review = Review(None, movie, "Trump's onto it!", datetime.today())

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_does_not_add_a_review_without_an_movie_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(2)
    review = Review(None, movie, "Trump's onto it!", datetime.today())

    user.add_review(review)

    with pytest.raises(RepositoryException):
        # Exception expected because the Movie doesn't refer to the Review.
        in_memory_repo.add_review(review)


def test_repository_can_retrieve_reviews(in_memory_repo):
    assert len(in_memory_repo.get_reviews()) == 2



